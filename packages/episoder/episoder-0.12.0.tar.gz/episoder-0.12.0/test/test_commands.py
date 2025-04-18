# episoder, https://code.ott.net/episoder
# -*- coding: utf8 -*-
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

from datetime import date, timedelta
from unittest import TestCase
from unittest.mock import MagicMock

from episoder.config import EpisoderConfig
from episoder.main import CommandWrapper
from episoder.options import OptionsLoader
from episoder.output import ColorfulRenderer, ColorlessRenderer


class CommandTest(TestCase):
    def setUp(self) -> None:
        self.cmd = OptionsLoader()
        self.config = EpisoderConfig()

    def _run(self, args: list[str]) -> MagicMock:
        options = self.cmd.parse_cmdline(args)
        self.cmd.validate(options)

        mock = MagicMock()
        command = CommandWrapper(options, self.config)
        # pylint: disable=protected-access
        command._episoder = mock
        command.run(options.func)
        return mock


class TestAddCommand(CommandTest):
    def test_add_show(self) -> None:
        mock = self._run(['add', 'http://foo'])
        mock.add_show.assert_called_with('http://foo')


class TestDisableCommand(CommandTest):
    def test_remove_show(self) -> None:
        mock = self._run(['disable', '62'])
        mock.disable_show.assert_called_with(62)


class TestEnableCommand(CommandTest):
    def test_enable_show(self) -> None:
        mock = self._run(['enable', '60'])
        mock.enable_show.assert_called_with(60)


class TestListCommand(CommandTest):
    def test_list_all_episodes(self) -> None:
        mock = self._run(['list'])
        mock.list_all_episodes.assert_called()

        args = mock.list_all_episodes.call_args[0]
        self.assertTrue(isinstance(args[0], ColorfulRenderer))
        self.assertEqual(args[1], date.today() - timedelta(1))
        self.assertEqual(args[2], 2)
        self.assertEqual(args[3], date.today() - timedelta(1))

    def test_list_episodes_no_color(self) -> None:
        mock = self._run(['list', '-C'])
        mock.list_all_episodes.assert_called()

        args = mock.list_all_episodes.call_args[0]
        self.assertTrue(isinstance(args[0], ColorlessRenderer))
        self.assertEqual(args[1], date.today() - timedelta(1))
        self.assertEqual(args[2], 2)
        self.assertEqual(args[3], date.today() - timedelta(1))

    def test_list_episodes_ignore_date(self) -> None:
        mock = self._run(['list', '-C', '-i'])
        mock.list_all_episodes.assert_called()

        args = mock.list_all_episodes.call_args[0]
        self.assertTrue(isinstance(args[0], ColorlessRenderer))
        self.assertEqual(args[1], date(1900, 1, 1))
        self.assertEqual(args[2], 109500)
        self.assertEqual(args[3], date.today() - timedelta(1))

    def test_search_episodes(self) -> None:
        mock = self._run(['list', '-s', 'foo'])
        mock.search_episodes.assert_called()

        args = mock.search_episodes.call_args[0]
        self.assertTrue(isinstance(args[0], ColorfulRenderer))
        self.assertEqual(args[1], 'foo')
        self.assertEqual(args[2], date.today() - timedelta(1))

    def test_search_episodes_no_color(self) -> None:
        mock = self._run(['list', '-s', 'foo', '-C'])
        mock.search_episodes.assert_called()

        args = mock.search_episodes.call_args[0]
        self.assertTrue(isinstance(args[0], ColorlessRenderer))
        self.assertEqual(args[1], 'foo')
        self.assertEqual(args[2], date.today() - timedelta(1))


class TestNotifyCommand(CommandTest):
    def test_notify(self) -> None:
        mock = self._run(['notify'])
        yesterday = date.today() - timedelta(1)
        mock.notify_upcoming.assert_called_with(self.config,
                                                yesterday, 2, False)

    def test_notify_with_base_date(self) -> None:
        mock = self._run(['notify', '-d', '2025-01-30'])
        mock.notify_upcoming.assert_called_with(self.config,
                                                date(2025, 1, 30), 2, False)

    def test_notify_with_base_date_and_number_of_days(self) -> None:
        mock = self._run(['notify', '-d', '2025-01-30', '-n', '14'])
        mock.notify_upcoming.assert_called_with(self.config,
                                                date(2025, 1, 30), 14, False)

    def test_notify_dry_run(self) -> None:
        mock = self._run(['notify', '--dryrun'])
        yesterday = date.today() - timedelta(1)
        mock.notify_upcoming.assert_called_with(self.config,
                                                yesterday, 2, True)

    def test_notify_dry_run_with_base_date(self) -> None:
        mock = self._run(['notify', '--dryrun', '-d', '2013-08-01'])
        mock.notify_upcoming.assert_called_with(self.config,
                                                date(2013, 8, 1), 2, True)

    def test_notify_dry_run_with_base_date_and_number_of_days(self) -> None:
        mock = self._run(['notify', '--dryrun', '-d', '2013-08-01', '-n', '8'])
        mock.notify_upcoming.assert_called_with(self.config,
                                                date(2013, 8, 1), 8, True)

    def test_notify_test(self) -> None:
        mock = self._run(['notify', '--test'])
        mock.test_notify.assert_called_with(self.config)


class TestRemoveCommand(CommandTest):
    def test_remove_show(self) -> None:
        mock = self._run(['remove', '23'])
        mock.remove_show.assert_called_with(23)


class TestSearchCommand(TestCase):
    def setUp(self) -> None:
        self.cmd = OptionsLoader()
        self.config = EpisoderConfig()

    def _run(self, args: list[str]) -> MagicMock:
        options = self.cmd.parse_cmdline(args)
        self.cmd.validate(options)

        mock = MagicMock()
        command = CommandWrapper(options, self.config)
        # pylint: disable=protected-access
        command._episoder = mock
        command.run(options.func)
        return mock

    def test_search(self) -> None:
        mock = self._run(['search', 'star trek'])
        mock.search.assert_called_with('star trek')


class TestShowsCommand(CommandTest):
    def test_active_shows(self) -> None:
        mock = self._run(['shows', '-a'])
        mock.print_active_shows.assert_called()

    def test_all_shows(self) -> None:
        mock = self._run(['shows'])
        mock.print_all_shows.assert_called()


class TestUpdateCommand(CommandTest):
    def test_update_single_show(self) -> None:
        mock = self._run(['update', '-s', '33'])
        yesterday = date.today() - timedelta(1)
        mock.update_show.assert_called_with(33, yesterday)

    def test_update_single_show_ignore_date(self) -> None:
        mock = self._run(['update', '-s', '34', '--nodate'])
        mock.update_show.assert_called_with(34, None)

    def test_update_all_shows(self) -> None:
        mock = self._run(['update', '-f', '-d', '2025-03-11'])
        mock.update_all_shows.assert_called_with(None, date(2025, 3, 11))

    def test_update_all_shows_ignore_date(self) -> None:
        mock = self._run(['update', '-f', '--nodate'])
        mock.update_all_shows.assert_called_with(None, None)

    def test_update_all_shows_limited_number(self) -> None:
        mock = self._run(['update', '-f', '-d', '2025-03-11', '-n', '5'])
        mock.update_all_shows.assert_called_with(5, date(2025, 3, 11))

    def test_update_expired_shows(self) -> None:
        mock = self._run(['update', '-d', '2025-03-13'])
        mock.update_expired_shows.assert_called_with(None, date(2025, 3, 13))

    def test_update_expired_shows_ignore_date(self) -> None:
        mock = self._run(['update', '-d', '2025-03-13', '--nodate'])
        mock.update_expired_shows.assert_called_with(None, None)

    def test_update_expired_shows_limited_number(self) -> None:
        mock = self._run(['update', '-d', '2025-03-13', '-n', '7'])
        mock.update_expired_shows.assert_called_with(7, date(2025, 3, 13))
