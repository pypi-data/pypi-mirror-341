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

from datetime import date
from unittest import TestCase
from unittest.mock import ANY, patch, MagicMock

from episoder.config import EpisoderConfig
from episoder.database import Show, Episode
from episoder.main import Episoder
from episoder.sources import setup_sources
from episoder.sources.thetvdb import TVDB, TVDBShowNotFoundError


class TestAddShow(TestCase):
    def setUp(self) -> None:
        setup_sources('episoder/test', '')

    @patch('episoder.main.Database')
    def test_add_new_epguides_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        database.get_show_by_url.return_value = None

        episoder.add_show('http://epguides.com/001')
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()

        database.add_show.assert_called_with(
                Show('Unknown Show', 'http://epguides.com/001'))
        database.commit.assert_called()

    @patch('episoder.main.Database')
    def test_add_new_tvcom_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        database.get_show_by_url.return_value = None

        episoder.add_show('71470')
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()

        database.add_show.assert_called_with(Show('Unknown Show', '71470'))
        database.commit.assert_called()

    @patch('episoder.main.Database')
    def test_add_new_invalid_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        database.get_show_by_url.return_value = None

        episoder.add_show('http://foo.bar')
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()

        database.add_show.assert_not_called()
        database.commit.assert_not_called()

    @patch('episoder.main.Database')
    def test_add_existing_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        database.get_show_by_url.return_value = Show('', '71470')

        episoder.add_show('71470')
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()

        database.add_show.assert_not_called()
        database.commit.assert_not_called()


class TestDisableShow(TestCase):
    @patch('episoder.main.Database')
    def test_disable_disabled_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        show = Show('', '71470')
        show.enabled = False
        database.get_show_by_id.return_value = show

        episoder.disable_show(3)
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()
        database.commit.assert_called()
        self.assertFalse(show.enabled)

    @patch('episoder.main.Database')
    def test_disable_enabled_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        show = Show('', '71470')
        show.enabled = True
        database.get_show_by_id.return_value = show

        episoder.disable_show(3)
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()
        database.commit.assert_called()
        self.assertFalse(show.enabled)

    @patch('episoder.main.Database')
    def test_disable_unknown_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        database.get_show_by_id.return_value = None

        episoder.disable_show(3)
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()
        database.commit.assert_not_called()


class TestEnableShow(TestCase):
    @patch('episoder.main.Database')
    def test_enable_disabled_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        show = Show('', '71470')
        show.enabled = False
        database.get_show_by_id.return_value = show

        episoder.enable_show(4)
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()
        database.commit.assert_called()
        self.assertTrue(show.enabled)

    @patch('episoder.main.Database')
    def test_enable_enabled_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        show = Show('', '71470')
        show.enabled = True
        database.get_show_by_id.return_value = show

        episoder.enable_show(4)
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()
        database.commit.assert_called()
        self.assertTrue(show.enabled)

    @patch('episoder.main.Database')
    def test_enable_unknown_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        database.get_show_by_id.return_value = None

        episoder.enable_show(4)
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()
        database.commit.assert_not_called()


class TestListAllEpisodes(TestCase):
    @patch('episoder.main.Database')
    def test_load_from_db(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        then = date(2001, 12, 31)
        today = date(2003, 2, 15)

        episoder.list_all_episodes(MagicMock(), then, 12, today)
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()
        database.get_episodes.assert_called_with(then, 12)

    @patch('episoder.main.Database')
    def test_render_results(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        renderer = MagicMock()
        then = date(2011, 12, 31)
        today = date(2012, 12, 31)

        ep1 = Episode("Episode 1", 1, 1, date(2014, 8, 10), "x", 1)
        ep2 = Episode("Episode 2", 1, 2, date(2014, 12, 1), "x", 2)
        database.get_episodes.return_value = [ep1, ep2]

        episoder.list_all_episodes(renderer, then, 3, today)
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()

        database.get_episodes.assert_called_with(then, 3)
        renderer.render.assert_called_with([ep1, ep2], today)


class TestNotifyUpcoming(TestCase):
    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.logging.getLogger')
    @patch('episoder.main.Database')
    def test_notify_without_mail_address(self, _: MagicMock,
                                         log_mock: MagicMock,
                                         notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        log = log_mock.return_value

        cfg = EpisoderConfig()
        cfg.email_to = None
        then = date(2001, 4, 3)

        episoder.notify_upcoming(cfg, then, 7, False)

        log.error.assert_called_with('No e-mail address configured')
        notifier_mock.assert_not_called()

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.logging.getLogger')
    @patch('episoder.main.Database')
    def test_notify_with_no_new_episodes(self, db_mock: MagicMock,
                                         log_mock: MagicMock,
                                         notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        log = log_mock.return_value
        database = db_mock.return_value

        database.get_episodes.return_value = []

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        then = date(2001, 4, 3)
        episoder.notify_upcoming(cfg, then, 7, False)

        database.get_episodes.assert_called_with(then, 7)
        log.info.assert_called_with('No new episodes')
        notifier_mock.assert_not_called()

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.Database')
    def test_notify_with_simple_config(self, db_mock: MagicMock,
                                       notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_mock.return_value

        ep1 = Episode("Episode 1", 1, 1, date(2014, 8, 10), "x", 1)
        ep2 = Episode("Episode 2", 1, 2, date(2014, 12, 1), "x", 2)
        show = Show('', '')
        ep1.show = show
        ep2.show = show
        database.get_episodes.return_value = [ep1, ep2]

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        cfg.email_server = 'smtp.example.org'
        cfg.email_port = 124

        then = date(2001, 4, 3)
        episoder.notify_upcoming(cfg, then, 7, False)

        database.get_episodes.assert_called_with(then, 7)
        notifier_mock.assert_called_with('smtp.example.org', 124)
        notifier = notifier_mock.return_value
        self.assertEqual(notifier.use_tls, False)
        notifier.send.assert_called_with(ANY, 'me@example.org')

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.Database')
    def test_notify_with_tls(self, db_mock: MagicMock,
                             notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_mock.return_value

        episode = Episode("Episode 1", 1, 1, date(2014, 8, 10), "x", 1)
        episode.show = Show('', '')
        database.get_episodes.return_value = [episode]

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        cfg.email_server = 'smtp.example.org'
        cfg.email_port = 124
        cfg.email_tls = True

        then = date(2001, 4, 3)
        episoder.notify_upcoming(cfg, then, 7, False)

        database.get_episodes.assert_called_with(then, 7)
        notifier_mock.assert_called_with('smtp.example.org', 124)
        notifier = notifier_mock.return_value
        self.assertEqual(notifier.use_tls, True)
        notifier.send.assert_called_with(ANY, 'me@example.org')

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.Database')
    def test_notify_with_only_username(self, db_mock: MagicMock,
                                       notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_mock.return_value

        episode = Episode("Episode 1", 1, 1, date(2014, 8, 10), "x", 1)
        episode.show = Show('', '')
        database.get_episodes.return_value = [episode]

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        cfg.email_server = 'smtp.example.org'
        cfg.email_port = 124
        cfg.email_username = 'myself'

        then = date(2001, 4, 3)
        episoder.notify_upcoming(cfg, then, 7, False)

        database.get_episodes.assert_called_with(then, 7)
        notifier_mock.assert_called_with('smtp.example.org', 124)
        notifier = notifier_mock.return_value
        self.assertEqual(notifier.use_tls, False)
        notifier.set_credentials.assert_not_called()
        notifier.send.assert_called_with(ANY, 'me@example.org')

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.Database')
    def test_notify_with_only_password(self, db_mock: MagicMock,
                                       notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_mock.return_value

        episode = Episode("Episode 1", 1, 1, date(2014, 8, 10), "x", 1)
        episode.show = Show('', '')
        database.get_episodes.return_value = [episode]

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        cfg.email_server = 'smtp.example.org'
        cfg.email_port = 124
        cfg.email_password = '****'

        then = date(2001, 4, 3)
        episoder.notify_upcoming(cfg, then, 7, False)

        database.get_episodes.assert_called_with(then, 7)
        notifier_mock.assert_called_with('smtp.example.org', 124)
        notifier = notifier_mock.return_value
        self.assertEqual(notifier.use_tls, False)
        notifier.set_credentials.assert_not_called()
        notifier.send.assert_called_with(ANY, 'me@example.org')

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.Database')
    def test_notify_with_auth(self, db_mock: MagicMock,
                              notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_mock.return_value

        episode = Episode("Episode 1", 1, 1, date(2014, 8, 10), "x", 1)
        episode.show = Show('', '')
        database.get_episodes.return_value = [episode]

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        cfg.email_server = 'smtp.example.org'
        cfg.email_port = 124
        cfg.email_username = 'myself'
        cfg.email_password = '****'

        then = date(2001, 4, 3)
        episoder.notify_upcoming(cfg, then, 7, False)

        database.get_episodes.assert_called_with(then, 7)
        notifier_mock.assert_called_with('smtp.example.org', 124)
        notifier = notifier_mock.return_value
        self.assertEqual(notifier.use_tls, False)
        notifier.set_credentials.assert_called_with('myself', '****')
        notifier.send.assert_called_with(ANY, 'me@example.org')

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.Database')
    def test_pretend_notify(self, db_mock: MagicMock,
                            notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_mock.return_value

        ep1 = Episode("Episode 1", 1, 1, date(2014, 8, 10), "x", 1)
        ep2 = Episode("Episode 2", 1, 2, date(2014, 12, 1), "x", 2)
        show = Show('', '')
        ep1.show = show
        ep2.show = show
        database.get_episodes.return_value = [ep1, ep2]

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        then = date(2001, 4, 3)
        episoder.notify_upcoming(cfg, then, 7, True)

        database.get_episodes.assert_called_with(then, 7)
        notifier_mock.assert_not_called()


def get_shows(status: list[int]) -> list[Show]:
    shows = []

    for i, show_status in enumerate(status):
        show = Show(f'{i}', f'http://{i}')
        show.status = show_status
        shows.append(show)

    return shows


class TestPrintActiveShows(TestCase):
    @patch('episoder.main.Episoder._print_shows')
    @patch('episoder.main.Database')
    def test_no_shows(self, db_constructor: MagicMock,
                      print_shows: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        database.get_shows.return_value = []

        episoder.print_active_shows()
        print_shows.assert_called_with([])

    @patch('episoder.main.Episoder._print_shows')
    @patch('episoder.main.Database')
    def test_print_running_shows(self, db_constructor: MagicMock,
                                 print_shows: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value

        [show_a, show_b, *_] = get_shows([Show.RUNNING, Show.RUNNING])
        database.get_shows.return_value = [show_a, show_b]

        episoder.print_active_shows()
        print_shows.assert_called_with([show_a, show_b])

    @patch('episoder.main.Episoder._print_shows')
    @patch('episoder.main.Database')
    def test_print_suspended_shows(self, db_constructor: MagicMock,
                                   print_shows: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value

        [show_a, show_b, *_] = get_shows([Show.RUNNING, Show.SUSPENDED])
        database.get_shows.return_value = [show_a, show_b]

        episoder.print_active_shows()
        print_shows.assert_called_with([show_a, show_b])

    @patch('episoder.main.Episoder._print_shows')
    @patch('episoder.main.Database')
    def test_print_ended_shows(self, db_constructor: MagicMock,
                               print_shows: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value

        [show_a, show_b, *_] = get_shows([Show.ENDED, Show.SUSPENDED])
        database.get_shows.return_value = [show_a, show_b]

        episoder.print_active_shows()
        print_shows.assert_called_with([show_b])


class TestPrintAllShows(TestCase):
    @patch('episoder.main.Episoder._print_shows')
    @patch('episoder.main.Database')
    def test_no_shows(self, db_constructor: MagicMock,
                      print_shows: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        database.get_shows.return_value = []

        episoder.print_all_shows()
        print_shows.assert_called_with([])

    @patch('episoder.main.Episoder._print_shows')
    @patch('episoder.main.Database')
    def test_print_running_shows(self, db_constructor: MagicMock,
                                 print_shows: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value

        [show_a, show_b, *_] = get_shows([Show.RUNNING, Show.RUNNING])
        database.get_shows.return_value = [show_a, show_b]

        episoder.print_all_shows()
        print_shows.assert_called_with([show_a, show_b])

    @patch('episoder.main.Episoder._print_shows')
    @patch('episoder.main.Database')
    def test_print_suspended_shows(self, db_constructor: MagicMock,
                                   print_shows: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value

        [show_a, show_b, *_] = get_shows([Show.RUNNING, Show.SUSPENDED])
        database.get_shows.return_value = [show_a, show_b]

        episoder.print_all_shows()
        print_shows.assert_called_with([show_a, show_b])

    @patch('episoder.main.Episoder._print_shows')
    @patch('episoder.main.Database')
    def test_print_ended_shows(self, db_constructor: MagicMock,
                               print_shows: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value

        [show_a, show_b, *_] = get_shows([Show.ENDED, Show.SUSPENDED])
        database.get_shows.return_value = [show_a, show_b]

        episoder.print_all_shows()
        print_shows.assert_called_with([show_a, show_b])


class TestSearch(TestCase):
    def setUp(self) -> None:
        setup_sources('episoder/test', '')

    @patch('episoder.main.parser_for')
    def test_search_show(self, parser_for: MagicMock) -> None:
        parser = MagicMock(spec=TVDB)
        parser_for.return_value = parser
        parser.lookup.return_value = []

        episoder = Episoder('/var/lib/episoder.db')
        episoder.search('star trek')

        parser.lookup.assert_called()

    @patch('episoder.main.parser_for')
    def test_search_show_not_found(self, parser_for: MagicMock) -> None:
        parser = MagicMock(spec=TVDB)
        parser_for.return_value = parser
        parser.lookup.side_effect = TVDBShowNotFoundError

        episoder = Episoder('/var/lib/episoder.db')
        episoder.search('star trek')

        parser.lookup.assert_called()


class TestSearchEpisodes(TestCase):
    @patch('episoder.main.Database')
    def test_search_db(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        today = date.today()

        episoder.search_episodes(MagicMock(), 'foo', today)
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()
        database.search.assert_called_with('foo')

    @patch('episoder.main.Database')
    def test_render_search_results(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        renderer = MagicMock()
        today = date.today()

        ep1 = Episode("Episode 1", 1, 1, date(2014, 8, 10), "x", 1)
        ep2 = Episode("Episode 2", 1, 2, date(2014, 12, 1), "x", 2)
        database.search.return_value = [ep1, ep2]

        episoder.search_episodes(renderer, 'bar', today)
        db_constructor.assert_called_with('/var/lib/episoder.db')
        database.migrate.assert_called()

        database.search.assert_called_with('bar')
        renderer.render.assert_called_with([ep1, ep2], today)


class TestTestNotify(TestCase):
    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.logging.getLogger')
    def test_notify_without_mail_address(self, log_mock: MagicMock,
                                         notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        log = log_mock.return_value

        cfg = EpisoderConfig()
        cfg.email_to = None

        episoder.test_notify(cfg)

        log.error.assert_called_with('No e-mail address configured')
        notifier_mock.assert_not_called()

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.logging.getLogger')
    def test_notify_with_simple_config(self, log_mock: MagicMock,
                                       notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        log = log_mock.return_value

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        cfg.email_server = 'smtp.example.org'
        cfg.email_port = 123

        episoder.test_notify(cfg)

        log.error.assert_not_called()
        notifier_mock.assert_called_with('smtp.example.org', 123)
        notifier = notifier_mock.return_value
        self.assertEqual(notifier.use_tls, False)
        notifier.set_credentials.assert_not_called()
        notifier.send.assert_called_with(ANY, 'me@example.org')

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.logging.getLogger')
    def test_notify_with_tls(self, log_mock: MagicMock,
                             notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        log = log_mock.return_value

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        cfg.email_server = 'smtp.example.org'
        cfg.email_port = 123
        cfg.email_tls = True

        episoder.test_notify(cfg)

        log.error.assert_not_called()
        notifier_mock.assert_called_with('smtp.example.org', 123)
        notifier = notifier_mock.return_value
        self.assertEqual(notifier.use_tls, True)
        notifier.set_credentials.assert_not_called()
        notifier.send.assert_called_with(ANY, 'me@example.org')

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.logging.getLogger')
    def test_notify_with_only_username(self, log_mock: MagicMock,
                                       notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        log = log_mock.return_value

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        cfg.email_server = 'smtp.example.org'
        cfg.email_port = 123
        cfg.email_username = 'myname'

        episoder.test_notify(cfg)

        log.error.assert_not_called()
        notifier_mock.assert_called_with('smtp.example.org', 123)
        notifier = notifier_mock.return_value
        self.assertEqual(notifier.use_tls, False)
        notifier.set_credentials.assert_not_called()
        notifier.send.assert_called_with(ANY, 'me@example.org')

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.logging.getLogger')
    def test_notify_with_only_password(self, log_mock: MagicMock,
                                       notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        log = log_mock.return_value

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        cfg.email_server = 'smtp.example.org'
        cfg.email_port = 123
        cfg.email_password = 's3kr1t'

        episoder.test_notify(cfg)

        log.error.assert_not_called()
        notifier_mock.assert_called_with('smtp.example.org', 123)
        notifier = notifier_mock.return_value
        self.assertEqual(notifier.use_tls, False)
        notifier.set_credentials.assert_not_called()
        notifier.send.assert_called_with(ANY, 'me@example.org')

    @patch('episoder.main.EmailNotifier')
    @patch('episoder.main.logging.getLogger')
    def test_notify_with_login(self, log_mock: MagicMock,
                               notifier_mock: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        log = log_mock.return_value

        cfg = EpisoderConfig()
        cfg.email_to = 'me@example.org'
        cfg.email_server = 'smtp.example.org'
        cfg.email_port = 123
        cfg.email_username = 'myname'
        cfg.email_password = 's3kr1t'

        episoder.test_notify(cfg)

        log.error.assert_not_called()
        notifier_mock.assert_called_with('smtp.example.org', 123)
        notifier = notifier_mock.return_value
        self.assertEqual(notifier.use_tls, False)
        notifier.set_credentials.assert_called_with('myname', 's3kr1t')
        notifier.send.assert_called_with(ANY, 'me@example.org')


class TestRemoveShow(TestCase):
    @patch('episoder.main.Database')
    def test_remove_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        show = Show('foo', 'http://bar')
        database.get_show_by_id.return_value = show

        episoder.remove_show(929810)
        database.remove_show.assert_called_with(show)
        database.commit.assert_called()

    @patch('episoder.main.Database')
    def test_remove_invalid_show(self, db_constructor: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        database.get_show_by_id.return_value = None

        episoder.remove_show(929810)
        database.remove_show.assert_not_called()
        database.commit.assert_not_called()


class TestUpdateAllShows(TestCase):
    @patch('episoder.main.parser_for')
    @patch('episoder.main.Database')
    def test_update_no_shows(self, db_constructor: MagicMock,
                             parser_for: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value

        database.get_enabled_shows.return_value = []
        episoder.update_all_shows(1, None)

        database.get_enabled_shows.assert_called()
        parser_for.assert_not_called()
        database.remove_after.assert_not_called()

    @patch('episoder.main.parser_for')
    @patch('episoder.main.Database')
    def test_update_unlimited_shows(self, db_constructor: MagicMock,
                                    parser_for: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value

        shows = [Show(str(x), str(x)) for x in range(10)]
        database.get_enabled_shows.return_value = shows
        episoder.update_all_shows(None, None)

        database.get_enabled_shows.assert_called()
        self.assertEqual(parser_for.call_count, 10)
        database.remove_before.assert_not_called()

    @patch('episoder.main.parser_for')
    @patch('episoder.main.Database')
    def test_update_limited_shows(self, db_constructor: MagicMock,
                                  parser_for: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        parser = parser_for.return_value

        shows = [Show(str(x), str(x)) for x in range(10)]
        database.get_enabled_shows.return_value = shows
        episoder.update_all_shows(6, None)

        database.get_enabled_shows.assert_called()
        self.assertEqual(parser_for.call_count, 6)
        self.assertEqual(parser.parse.call_count, 6)
        database.remove_before.assert_not_called()

    @patch('episoder.main.parser_for')
    @patch('episoder.main.Database')
    def test_update_shows_after_date(self, db_constructor: MagicMock,
                                     parser_for: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        then = date(1991, 2, 9)
        parser = parser_for.return_value

        shows = [Show(str(x), str(x)) for x in range(3)]
        database.get_enabled_shows.return_value = shows
        episoder.update_all_shows(None, then)

        database.get_enabled_shows.assert_called()
        self.assertEqual(parser_for.call_count, 3)
        self.assertEqual(parser.parse.call_count, 3)
        self.assertEqual(database.remove_before.call_count, 3)
        database.remove_before.assert_called_with(then, shows[2])


class TestUpdateExpiredShows(TestCase):
    @patch('episoder.main.parser_for')
    @patch('episoder.main.Database')
    def test_update_no_shows(self, db_constructor: MagicMock,
                             parser_for: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value

        database.get_expired_shows.return_value = []
        episoder.update_expired_shows(1, None)

        database.get_expired_shows.assert_called()
        parser_for.assert_not_called()
        database.remove_after.assert_not_called()

    @patch('episoder.main.parser_for')
    @patch('episoder.main.Database')
    def test_update_unlimited_shows(self, db_constructor: MagicMock,
                                    parser_for: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value

        shows = [Show(str(x), str(x)) for x in range(10)]
        database.get_expired_shows.return_value = shows
        episoder.update_expired_shows(None, None)

        database.get_expired_shows.assert_called()
        self.assertEqual(parser_for.call_count, 10)
        database.remove_before.assert_not_called()

    @patch('episoder.main.parser_for')
    @patch('episoder.main.Database')
    def test_update_limited_shows(self, db_constructor: MagicMock,
                                  parser_for: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        parser = parser_for.return_value

        shows = [Show(str(x), str(x)) for x in range(10)]
        database.get_expired_shows.return_value = shows
        episoder.update_expired_shows(6, None)

        database.get_expired_shows.assert_called()
        self.assertEqual(parser_for.call_count, 6)
        self.assertEqual(parser.parse.call_count, 6)
        database.remove_before.assert_not_called()

    @patch('episoder.main.parser_for')
    @patch('episoder.main.Database')
    def test_update_shows_after_date(self, db_constructor: MagicMock,
                                     parser_for: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        then = date(1991, 2, 9)
        parser = parser_for.return_value

        shows = [Show(str(x), str(x)) for x in range(3)]
        database.get_expired_shows.return_value = shows
        episoder.update_expired_shows(None, then)

        database.get_expired_shows.assert_called()
        self.assertEqual(parser_for.call_count, 3)
        self.assertEqual(parser.parse.call_count, 3)
        self.assertEqual(database.remove_before.call_count, 3)
        database.remove_before.assert_called_with(then, shows[2])


class TestUpdateShow(TestCase):
    @patch('episoder.main.parser_for')
    @patch('episoder.main.Database')
    def test_update_show_without_start_date(self, db_constructor: MagicMock,
                                            parser_for: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value

        show = Show('some', 'http://show')
        database.get_show_by_id.return_value = show
        episoder.update_show(1, None)

        database.get_show_by_id.assert_called_with(1)
        parser_for.assert_called_once_with('http://show')

        parser = parser_for.return_value
        parser.parse.assert_called_with(show, database)
        database.remove_before.assert_not_called()

    @patch('episoder.main.parser_for')
    @patch('episoder.main.Database')
    def test_update_show_with_start_date(self, db_constructor: MagicMock,
                                         parser_for: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        then = date(2024, 12, 9)

        show = Show('some', 'http://show')
        database.get_show_by_id.return_value = show
        episoder.update_show(1, then)

        database.get_show_by_id.assert_called_with(1)
        parser_for.assert_called_once_with('http://show')

        parser = parser_for.return_value
        parser.parse.assert_called_with(show, database)
        database.remove_before.assert_called_with(then, show)

    @patch('episoder.main.parser_for')
    @patch('episoder.main.logging.getLogger')
    @patch('episoder.main.Database')
    def test_update_invalid_show(self, db_constructor: MagicMock,
                                 log_mock: MagicMock,
                                 parser_for: MagicMock) -> None:
        episoder = Episoder('/var/lib/episoder.db')
        database = db_constructor.return_value
        log = log_mock.return_value

        database.get_show_by_id.return_value = None
        episoder.update_show(99, date.today())

        database.get_show_by_id.assert_called_with(99)
        log.error.assert_called_with('Show not found')
        parser_for.assert_not_called()
