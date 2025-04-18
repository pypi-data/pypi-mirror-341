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

from argparse import ArgumentParser, Namespace
from datetime import date, timedelta
from os import environ, path
from re import match

from episoder.version import __version__


class OptionsLoader:
    def __init__(self) -> None:
        self._parser = ArgumentParser()

        self._parser.set_defaults(func=None)
        self._add_global_options(self._parser)

        yesterday = date.today() - timedelta(1)
        self._commands = self._parser.add_subparsers(help='commands')
        self._add_adding_options()
        self._add_disable_options()
        self._add_enable_options()
        self._add_list_options(yesterday)
        self._add_removing_options()
        self._add_search_options()
        self._add_shows_options()
        self._add_notify_options(yesterday)
        self._add_update_options(yesterday)

    def _add_adding_options(self) -> None:
        parser = self._commands.add_parser('add', help='Add a show')
        parser.add_argument('show', action='store',
                            help='show to add (TVDB ID or epguides.com URL)')
        parser.set_defaults(func='add')

    def _add_disable_options(self) -> None:
        parser = self._commands.add_parser('disable',
                                           help='Disable updates for a show')
        parser.add_argument('show', action='store', type=int,
                            help='the show ID to disable updates for')
        parser.set_defaults(func='disable')

    def _add_enable_options(self) -> None:
        parser = self._commands.add_parser('enable',
                                           help='Enable updates for a show')
        parser.add_argument('show', action='store', type=int,
                            help='the show ID to enable updates for')
        parser.set_defaults(func='enable')

    def _add_list_options(self, yesterday: date) -> None:
        parser = self._commands.add_parser('list',
                                           help='Show upcoming episodes')
        parser.add_argument('-C', '--nocolor', action='store_true',
                            help='do not use colors')
        parser.add_argument('-d', metavar='YYYY-MM-DD|n', dest='date',
                            default=yesterday.strftime('%Y-%m-%d'),
                            help='only show episodes after this date '
                            '/ n days back')
        parser.add_argument('-n', '--days', type=int, default=2,
                            help='number of future days to show (default: 2)')
        parser.add_argument('-i', '--nodate', action='store_true',
                            help='ignore date, show all episodes')
        parser.add_argument('-s', dest='search',
                            help='search episodes')
        parser.set_defaults(func='episodes')

    def _add_removing_options(self) -> None:
        parser = self._commands.add_parser('remove',
                                           help='Remove a show from the db')
        parser.add_argument('show', action='store', type=int,
                            help='the show ID to remove')
        parser.set_defaults(func='remove')

    def _add_search_options(self) -> None:
        parser = self._commands.add_parser('search',
                                           help='Find shows on TVDB')
        parser.add_argument('keyword', action='store',
                            help='search string')
        parser.set_defaults(func='search')

    def _add_shows_options(self) -> None:
        parser = self._commands.add_parser('shows',
                                           help='List shows in the database')
        parser.add_argument('-a', '--active', action='store_true',
                            help='only lists shows that are running/suspended')
        parser.set_defaults(func='shows')

    def _add_notify_options(self, yesterday: date) -> None:
        parser = self._commands.add_parser('notify',
                                           help='Send e-mail notifications '
                                           'about new episodes')
        parser.add_argument('-d', metavar='YYYY-MM-DD|n', dest='date',
                            default=yesterday.strftime('%Y-%m-%d'),
                            help='only show episodes prior to this date '
                            'or n days back')
        parser.add_argument('-n', '--days', type=int, default=2,
                            help='number of future days to show (default: 2)')
        parser.add_argument('--dryrun', action='store_true', default=False,
                            help='pretend, do not send email')
        parser.add_argument('--test', action='store_true', default=False,
                            help='send a test message')
        parser.set_defaults(func='notify')

    def _add_update_options(self, yesterday: date) -> None:
        parser = self._commands.add_parser('update',
                                           help='Update the database')
        parser.add_argument('-d', metavar='YYYY-MM-DD|n', dest='date',
                            default=yesterday.strftime('%Y-%m-%d'),
                            help='remove episodes prior to this date '
                            'or n days back')
        parser.add_argument('-f', '--force', action='store_true',
                            help='force update, disregard last update time')
        parser.add_argument('-i', '--nodate', action='store_true',
                            help='ignore date, do not remove old episodes')
        parser.add_argument('-s', '--show', metavar='id', type=int,
                            help='only update the show with this id')
        parser.add_argument('-n', '--num', metavar='num', type=int,
                            help='update no more than num shows at a time')
        parser.set_defaults(func='update')

    def _add_global_options(self, parser: ArgumentParser) -> None:
        parser.add_argument('-c', metavar='file', action='store',
                            default=path.join(environ['HOME'], '.episoder'),
                            help='use configuration from file')
        parser.add_argument('-l', metavar='file', dest='logfile',
                            action='store',
                            help='log to file instead of stdout')
        parser.add_argument('-V', '--version', action='version',
                            version=f'episoder {__version__}',
                            help='show version information')

        group = parser.add_mutually_exclusive_group()
        group.add_argument('-v', '--verbose', action='store_true',
                           help='verbose operation')
        group.add_argument('-d', '--debug', action='store_true',
                           help='debug (very verbose) operation')

    # may raise SystemExit if arguments are invalid
    def parse_cmdline(self, cmdline: list[str]) -> Namespace:
        return self._parser.parse_args(cmdline)

    def help(self) -> None:
        self._parser.print_usage()

    def _replace_parsed_date(self, options: Namespace) -> None:
        if options.date.isdigit():
            daysback = int(options.date)
            options.date = date.today() - timedelta(daysback)
        elif match('^[0-9]{4}(-[0-9]{2}){2}$', options.date):
            (year, month, day) = options.date.split('-')
            options.date = date(int(year), int(month), int(day))
        else:
            self._parser.error(f'{options.date}: Invalid date')

    # may raise SystemExit if options are invalid
    def validate(self, options: Namespace) -> None:
        if options.func is None:
            self._parser.error('Nothing to do')

        if hasattr(options, 'date'):
            self._replace_parsed_date(options)
