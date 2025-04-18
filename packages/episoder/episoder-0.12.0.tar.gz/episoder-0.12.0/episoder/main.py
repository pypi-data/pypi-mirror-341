#!/usr/bin/env python

# episoder, https://code.ott.net/episoder
#
# Copyright (C) 2004-2025 Stefan Ott. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import functools
import logging
import sys

from argparse import Namespace
from datetime import date
from traceback import print_exc
from typing import Any, Callable, Optional

from .config import ConfigLoader, EpisoderConfig
from .database import Show
from .episoder import Database
from .options import OptionsLoader
from .output import ColorfulRenderer, ColorlessRenderer, EmailNotifier
from .output import ConsoleRenderer, NewEpisodesNotification, SmtpTestMessage
from .sources import parser_for, setup_sources
from .sources.thetvdb import TVDB, TVDBShowNotFoundError


def configure_logging(args: Namespace) -> None:
    if args.debug:
        loglevel = logging.DEBUG
    elif args.verbose:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING

    if args.logfile:
        logging.basicConfig(level=loglevel, filename=args.logfile)
    else:
        logging.basicConfig(level=loglevel)


class DatabaseWrapper:
    def __init__(self, db_file: str) -> None:
        self._db_file = db_file
        self._conn: Optional[Database] = None

    def __enter__(self) -> Database:
        self._conn = Database(self._db_file)
        self._conn.migrate()
        return self._conn

    def __exit__(self, _: int, __: int, ___: int) -> None:
        assert self._conn is not None
        self._conn.close()


def with_db(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped(*args: str, **kwargs: str) -> Any:
        self = args[0]
        assert isinstance(self, Episoder)

        self.database = Database(self.db_file)
        self.database.migrate()
        result = func(*args, **kwargs)
        self.database.close()

        return result

    return wrapped


class Episoder:
    def __init__(self, db_file: str) -> None:
        self.db_file = db_file
        self.database: Optional[Database] = None
        self._database = DatabaseWrapper(db_file)
        self._log = logging.getLogger('Episoder')

    @with_db
    def add_show(self, url: str) -> None:
        assert self.database is not None
        show = self.database.get_show_by_url(url)

        if show:
            self._log.error('A show with that url already exists')
        elif not parser_for(url):
            self._log.error('Invalid show url/id: %s', url)
        else:
            show = Show('Unknown Show', url)
            self.database.add_show(show)
            self.database.commit()

    def _set_enabled(self, show_id: int, enabled: bool) -> None:
        assert self.database is not None
        show = self.database.get_show_by_id(show_id)

        if not show:
            self._log.error('There is no show with id=%d', show_id)
            return

        show.enabled = enabled
        self.database.commit()

    @with_db
    def disable_show(self, show_id: int) -> None:
        assert self.database is not None
        self._set_enabled(show_id, False)

    @with_db
    def enable_show(self, show_id: int) -> None:
        assert self.database is not None
        self._set_enabled(show_id, True)

    @with_db
    def list_all_episodes(self, out: ConsoleRenderer, startdate: date,
                          n_days: int, today: date) -> None:
        assert self.database is not None
        episodes = self.database.get_episodes(startdate, n_days)
        out.render(episodes, today)

    @with_db
    def search_episodes(self, out: ConsoleRenderer, term: str,
                        today: date) -> None:
        assert self.database is not None
        episodes = self.database.search(term)
        out.render(episodes, today)

    def _get_notifier(self, cfg: EpisoderConfig) -> EmailNotifier:
        notifier = EmailNotifier(cfg.email_server, cfg.email_port)
        notifier.use_tls = cfg.email_tls

        if cfg.email_username and cfg.email_password:
            notifier.set_credentials(cfg.email_username, cfg.email_password)

        return notifier

    @with_db
    def notify_upcoming(self, cfg: EpisoderConfig, base_date: date,
                        days: int, pretend: bool) -> None:
        assert self.database is not None

        if cfg.email_to is None:
            self._log.error('No e-mail address configured')
            return

        all_episodes = self.database.get_episodes(base_date, days)
        fresh = [e for e in all_episodes if not e.notified]

        if len(fresh) < 1:
            self._log.info('No new episodes')
            return

        msg = NewEpisodesNotification(fresh, cfg.format, cfg.dateformat)

        if pretend:
            print(msg)
        else:
            notifier = self._get_notifier(cfg)
            notifier.send(msg, cfg.email_to)
            for episode in fresh:
                episode.notified = date.today()
            self.database.commit()

    def test_notify(self, cfg: EpisoderConfig) -> None:
        if cfg.email_to is None:
            self._log.error('No e-mail address configured')
        else:
            notifier = self._get_notifier(cfg)
            msg = SmtpTestMessage()
            notifier.send(msg, cfg.email_to)

    def _print_shows(self, shows: list[Show]) -> None:
        status_strings = ['?Invalid', 'Running', 'Suspended', 'Ended']
        enabled_strings = ['Disabled', 'Enabled']

        for show in shows:
            status = status_strings[show.status or 0]
            enabled = enabled_strings[show.enabled]

            print(f'[{show.id:4d}] {show.url}')
            print(f'       {show.name}, {status}, {enabled}')
            print(f'       Last update: {show.updated}')
            print(f'       Episodes: {len(show.episodes)}')

    @with_db
    def print_active_shows(self) -> None:
        assert self.database is not None
        shows = [show for show in self.database.get_shows()
                 if show.status != Show.ENDED]
        self._print_shows(shows)

    @with_db
    def print_all_shows(self) -> None:
        assert self.database is not None
        shows = self.database.get_shows()
        self._print_shows(shows)

    @with_db
    def remove_show(self, show_id: int) -> None:
        assert self.database is not None
        show = self.database.get_show_by_id(show_id)

        if show:
            self.database.remove_show(show)
            self.database.commit()
        else:
            self._log.error('No such show')

    def search(self, keyword: str) -> None:
        tvdb = parser_for('123')  # numeric IDs are TVDB entries
        assert isinstance(tvdb, TVDB)

        try:
            print('ID\tName\n-------\t--------------------')
            for show in tvdb.lookup(keyword):
                print(f'{show.url}\t{show.name}')

        except TVDBShowNotFoundError:
            print('Nothing found')

    def _update_shows(self, shows: list[Show], after: Optional[date]) -> None:
        assert self.database is not None
        for show in shows:
            try:
                parser = parser_for(show.url)
                assert parser is not None
                parser.parse(show, self.database)
            # pylint: disable=broad-exception-caught
            except Exception:
                self._log.error('Error parsing %s', show)
                print_exc()
                self.database.rollback()

            if after:
                self.database.remove_before(after, show)

    @with_db
    def update_show(self, show_id: int, start_date: Optional[date]) -> None:
        assert self.database is not None
        show = self.database.get_show_by_id(show_id)

        if show:
            self._update_shows([show], start_date)
        else:
            self._log.error('Show not found')

    @with_db
    def update_all_shows(self, max_number_of_shows: Optional[int],
                         start_date: Optional[date]) -> None:
        assert self.database is not None
        shows = self.database.get_enabled_shows()
        self._update_shows(shows[:max_number_of_shows], start_date)

    @with_db
    def update_expired_shows(self, max_number_of_shows: Optional[int],
                             start_date: Optional[date]) -> None:
        assert self.database is not None
        shows = self.database.get_expired_shows()

        if len(shows) > 0:
            self._update_shows(shows[:max_number_of_shows], start_date)
        else:
            self._log.info('None of your shows need to be updated')


class CommandWrapper:
    def __init__(self, args: Namespace, cfg: EpisoderConfig) -> None:
        self._args = args
        self._cfg = cfg
        self._log = logging.getLogger('CommandWrapper')
        self._episoder = Episoder(self._cfg.datafile)

    def add(self) -> None:
        url = self._args.show
        self._episoder.add_show(url)

    def enable(self) -> None:
        show = self._args.show
        self._episoder.enable_show(show)

    def disable(self) -> None:
        show = self._args.show
        self._episoder.disable_show(show)

    def shows(self) -> None:
        if self._args.active:
            self._episoder.print_active_shows()
        else:
            self._episoder.print_all_shows()

    def remove(self) -> None:
        show = self._args.show
        self._episoder.remove_show(show)

    def update(self) -> None:
        if self._args.nodate:
            start_date = None
        else:
            start_date = self._args.date

        if self._args.show:
            self._episoder.update_show(self._args.show, start_date)
        elif self._args.force:
            self._episoder.update_all_shows(self._args.num, start_date)
        else:
            self._episoder.update_expired_shows(self._args.num, start_date)

    def notify(self) -> None:
        if self._args.test:
            self._episoder.test_notify(self._cfg)
        else:
            base_date = self._args.date
            days = self._args.days
            dry_run = self._args.dryrun
            self._episoder.notify_upcoming(self._cfg, base_date, days, dry_run)

    def episodes(self) -> None:
        out: ConsoleRenderer
        if self._args.nocolor:
            out = ColorlessRenderer(self._cfg.format, self._cfg.dateformat)
        else:
            out = ColorfulRenderer(self._cfg.format, self._cfg.dateformat)

        if self._args.search:
            search_term = self._args.search
            base_date = self._args.date
            self._episoder.search_episodes(out, search_term, base_date)
        else:
            if self._args.nodate:
                startdate = date(1900, 1, 1)
                n_days = 109500  # should be fine until late 21xx :)
            else:
                startdate = self._args.date
                n_days = self._args.days

            base_date = self._args.date
            self._episoder.list_all_episodes(out, startdate, n_days, base_date)

    def search(self) -> None:
        keyword = self._args.keyword
        self._episoder.search(keyword)

    def run(self, command: str) -> None:
        func = getattr(self, command)
        func()


def main() -> None:
    loader = OptionsLoader()
    options = loader.parse_cmdline(sys.argv[1:])
    loader.validate(options)
    configure_logging(options)

    config_loader = ConfigLoader()
    cfg = config_loader.load(options.c)
    config_loader.validate(cfg)

    setup_sources(cfg.agent, cfg.tvdb_key)

    command = CommandWrapper(options, cfg)
    command.run(options.func)


if __name__ == '__main__':
    main()
