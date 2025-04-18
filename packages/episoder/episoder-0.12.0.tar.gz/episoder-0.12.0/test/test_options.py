# episoder, https://code.ott.net/episoder
# -*- coding: utf8 -*-
# # Copyright (C) 2004-2025 Stefan Ott. All rights reserved.
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
from os.path import basename
from unittest import TestCase

from episoder.options import OptionsLoader


class TestAddShow(TestCase):
    def setUp(self) -> None:
        self.loader = OptionsLoader()

    def test_needs_show_parameter(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['add'])

    def test_add_show_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['add'])

    def test_add_show_by_id(self) -> None:
        opt = self.loader.parse_cmdline(['add', '425711'])
        self.assertEqual(opt.func, 'add')
        self.assertEqual(opt.show, '425711')

    def test_add_show_by_url(self) -> None:
        opt = self.loader.parse_cmdline(['add',
                                         'https://epguides.com/frasier/'])
        self.assertEqual(opt.func, 'add')
        self.assertEqual(opt.show, 'https://epguides.com/frasier/')


class TestRemoveShow(TestCase):
    def setUp(self) -> None:
        self.loader = OptionsLoader()

    def test_needs_show_parameter(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['remove'])

    def test_remove_show_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['remove'])

    def test_remove_show(self) -> None:
        opt = self.loader.parse_cmdline(['remove', '42'])
        self.assertEqual(opt.func, 'remove')
        self.assertEqual(opt.show, 42)


class TestEnableShow(TestCase):
    def setUp(self) -> None:
        self.loader = OptionsLoader()

    def test_needs_show_parameter(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['enable'])

    def test_enable_show_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['enable'])

    def test_enable_show(self) -> None:
        opt = self.loader.parse_cmdline(['enable', '3353'])
        self.assertEqual(opt.func, 'enable')
        self.assertEqual(opt.show, 3353)


class TestDisableShow(TestCase):
    def setUp(self) -> None:
        self.loader = OptionsLoader()

    def test_needs_show_parameter(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['disable'])

    def test_disable_show_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['disable'])

    def test_disable_show(self) -> None:
        opt = self.loader.parse_cmdline(['disable', '3455'])
        self.assertEqual(opt.func, 'disable')
        self.assertEqual(opt.show, 3455)


class TestListEpisodes(TestCase):
    def setUp(self) -> None:
        self.loader = OptionsLoader()

    def test_list_defaults(self) -> None:
        opt = self.loader.parse_cmdline(['list'])

        self.assertEqual(opt.func, 'episodes')
        self.assertFalse(opt.nocolor)

        yesterday = date.today() - timedelta(days=1)
        self.assertEqual(opt.date, yesterday.strftime('%Y-%m-%d'))
        self.assertEqual(opt.days, 2)
        self.assertFalse(opt.nodate)

    def test_list_without_colors(self) -> None:
        opt = self.loader.parse_cmdline(['list', '-C'])
        self.assertEqual(opt.func, 'episodes')
        self.assertTrue(opt.nocolor)

        opt = self.loader.parse_cmdline(['list', '--nocolor'])
        self.assertEqual(opt.func, 'episodes')
        self.assertTrue(opt.nocolor)

    def test_date_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['list', '-d'])

    def test_relative_date(self) -> None:
        opt = self.loader.parse_cmdline(['list', '-d', '6'])
        self.assertEqual(opt.func, 'episodes')
        self.assertEqual(opt.date, '6')

    def test_absolute_date(self) -> None:
        opt = self.loader.parse_cmdline(['list', '-d', '2025-03-08'])
        self.assertEqual(opt.func, 'episodes')
        self.assertEqual(opt.date, '2025-03-08')

    def test_set_number_of_days_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['list', '-n'])

    def test_set_number_of_days(self) -> None:
        opt = self.loader.parse_cmdline(['list', '-n', '14'])
        self.assertEqual(opt.func, 'episodes')
        self.assertEqual(opt.days, 14)

    def test_ignore_date(self) -> None:
        opt = self.loader.parse_cmdline(['list', '-i'])
        self.assertEqual(opt.func, 'episodes')
        self.assertTrue(opt.nodate)

        opt = self.loader.parse_cmdline(['list', '--nodate'])
        self.assertEqual(opt.func, 'episodes')
        self.assertTrue(opt.nodate)

    def test_search_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['list', '-s'])

    def test_search(self) -> None:
        opt = self.loader.parse_cmdline(['list', '-s', 'Columbo'])
        self.assertEqual(opt.func, 'episodes')
        self.assertEqual(opt.search, 'Columbo')

    def test_combination_of_options(self) -> None:
        opt = self.loader.parse_cmdline(['list', '-s', 'Star Trek', '-i',
                                         '-n', '12'])
        self.assertEqual(opt.func, 'episodes')
        self.assertEqual(opt.search, 'Star Trek')
        self.assertEqual(opt.days, 12)
        self.assertTrue(opt.nodate)


class TestSearchForShow(TestCase):
    def setUp(self) -> None:
        self.loader = OptionsLoader()

    def test_search_needs_keyword(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['search'])

    def test_search_with_keyword(self) -> None:
        opt = self.loader.parse_cmdline(['search', 'star trek'])
        self.assertEqual(opt.func, 'search')
        self.assertEqual(opt.keyword, 'star trek')


class TestListShows(TestCase):
    def setUp(self) -> None:
        self.loader = OptionsLoader()

    def test_list_all_shows(self) -> None:
        opt = self.loader.parse_cmdline(['shows'])
        self.assertEqual(opt.func, 'shows')
        self.assertFalse(opt.active)

    def test_list_active_shows(self) -> None:
        opt = self.loader.parse_cmdline(['shows', '-a'])
        self.assertEqual(opt.func, 'shows')
        self.assertTrue(opt.active)

        opt = self.loader.parse_cmdline(['shows', '--active'])
        self.assertEqual(opt.func, 'shows')
        self.assertTrue(opt.active)


class TestUpdateDatabase(TestCase):
    def setUp(self) -> None:
        self.loader = OptionsLoader()

    def test_default_options(self) -> None:
        opt = self.loader.parse_cmdline(['update'])
        self.assertEqual(opt.func, 'update')

        yesterday = date.today() - timedelta(days=1)
        self.assertEqual(opt.date, yesterday.strftime('%Y-%m-%d'))
        self.assertFalse(opt.force)
        self.assertFalse(opt.nodate)
        self.assertIsNone(opt.show)
        self.assertIsNone(opt.num)

    def test_date_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['update', '-d'])

    def test_use_absolute_date(self) -> None:
        opt = self.loader.parse_cmdline(['update', '-d', '2013-04-01'])
        self.assertEqual(opt.func, 'update')
        self.assertEqual(opt.date, '2013-04-01')

    def test_use_relative_date(self) -> None:
        opt = self.loader.parse_cmdline(['update', '-d', '14'])
        self.assertEqual(opt.func, 'update')
        self.assertEqual(opt.date, '14')

    def test_force(self) -> None:
        opt = self.loader.parse_cmdline(['update', '-f'])
        self.assertEqual(opt.func, 'update')
        self.assertTrue(opt.force)

    def test_ignore_date(self) -> None:
        opt = self.loader.parse_cmdline(['update', '-i'])
        self.assertEqual(opt.func, 'update')
        self.assertTrue(opt.nodate)

        opt = self.loader.parse_cmdline(['update', '--nodate'])
        self.assertEqual(opt.func, 'update')
        self.assertTrue(opt.nodate)

    def test_show_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['update', '-s'])

    def test_specify_show(self) -> None:
        opt = self.loader.parse_cmdline(['update', '-s', '145'])
        self.assertEqual(opt.func, 'update')
        self.assertEqual(opt.show, 145)

        opt = self.loader.parse_cmdline(['update', '--show', '147'])
        self.assertEqual(opt.func, 'update')
        self.assertEqual(opt.show, 147)

    def test_number_of_shows_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['update', '-n'])

    def test_number_of_shows(self) -> None:
        opt = self.loader.parse_cmdline(['update', '-n', '5'])
        self.assertEqual(opt.func, 'update')
        self.assertEqual(opt.num, 5)

        opt = self.loader.parse_cmdline(['update', '--num', '7'])
        self.assertEqual(opt.func, 'update')
        self.assertEqual(opt.num, 7)

    def test_combination_of_options(self) -> None:
        opt = self.loader.parse_cmdline(['update', '-n', '25', '-i', '-f'])
        self.assertEqual(opt.func, 'update')
        self.assertEqual(opt.num, 25)
        self.assertTrue(opt.nodate)
        self.assertTrue(opt.force)


class TestNotify(TestCase):
    def setUp(self) -> None:
        self.loader = OptionsLoader()

    def test_default_options(self) -> None:
        opt = self.loader.parse_cmdline(['notify'])
        self.assertEqual(opt.func, 'notify')

        yesterday = date.today() - timedelta(days=1)
        self.assertEqual(opt.date, yesterday.strftime('%Y-%m-%d'))
        self.assertEqual(opt.days, 2)
        self.assertFalse(opt.dryrun)
        self.assertFalse(opt.test)

    def test_date_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['notify', '-d'])

    def test_use_absolute_date(self) -> None:
        opt = self.loader.parse_cmdline(['notify', '-d', '2013-04-01'])
        self.assertEqual(opt.func, 'notify')
        self.assertEqual(opt.date, '2013-04-01')

    def test_use_relative_date(self) -> None:
        opt = self.loader.parse_cmdline(['notify', '-d', '14'])
        self.assertEqual(opt.func, 'notify')
        self.assertEqual(opt.date, '14')

    def test_number_of_future_days_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['notify', '-n'])

        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['notify', '--days'])

    def test_number_of_future_days(self) -> None:
        opt = self.loader.parse_cmdline(['notify', '-n', '6'])
        self.assertEqual(opt.func, 'notify')
        self.assertEqual(opt.days, 6)

        opt = self.loader.parse_cmdline(['notify', '--days', '19'])
        self.assertEqual(opt.func, 'notify')
        self.assertEqual(opt.days, 19)

    def test_specific_show_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['notify', '-s'])

        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['notify', '--show'])

    def test_dry_run(self) -> None:
        opt = self.loader.parse_cmdline(['notify', '--dryrun'])
        self.assertEqual(opt.func, 'notify')
        self.assertTrue(opt.dryrun)

    def test_notify_test(self) -> None:
        opt = self.loader.parse_cmdline(['notify', '--test'])
        self.assertEqual(opt.func, 'notify')
        self.assertTrue(opt.test)


class GlobalOptionsTests(TestCase):
    def setUp(self) -> None:
        self.loader = OptionsLoader()

    def test_default_options(self) -> None:
        opt = self.loader.parse_cmdline([])
        self.assertEqual(basename(opt.c), '.episoder')
        self.assertFalse(opt.debug)
        self.assertFalse(opt.verbose)
        self.assertIsNone(opt.func)
        self.assertIsNone(opt.logfile)

    def test_set_config_file_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['-c'])

    def test_set_config_file(self) -> None:
        opt = self.loader.parse_cmdline(['-c', '/tmp/episoder.conf'])
        self.assertEqual(opt.c, '/tmp/episoder.conf')

    def test_verbose_mode(self) -> None:
        opt = self.loader.parse_cmdline(['-v'])
        self.assertTrue(opt.verbose)

        opt = self.loader.parse_cmdline(['--verbose'])
        self.assertTrue(opt.verbose)

    def test_debug_mode(self) -> None:
        opt = self.loader.parse_cmdline(['-d'])
        self.assertTrue(opt.debug)

        opt = self.loader.parse_cmdline(['--debug'])
        self.assertTrue(opt.debug)

    def test_log_file_needs_argument(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['-l'])

    def test_log_file(self) -> None:
        opt = self.loader.parse_cmdline(['-l', '/tmp/episoder.log'])
        self.assertEqual(opt.logfile, '/tmp/episoder.log')

    def test_show_version(self) -> None:
        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['--version'])

        with self.assertRaises(SystemExit):
            self.loader.parse_cmdline(['-V'])


class ValidateOptionsTest(TestCase):
    def setUp(self) -> None:
        self.loader = OptionsLoader()

    def test_validate_valid_options(self) -> None:
        opt = self.loader.parse_cmdline(['enable', '3353'])
        self.loader.validate(opt)

    def test_validate_command_missing(self) -> None:
        opt = self.loader.parse_cmdline([])
        with self.assertRaises(SystemExit):
            self.loader.validate(opt)

    def test_validate_replaces_relative_date(self) -> None:
        opt = self.loader.parse_cmdline(['list', '-d', '6'])
        self.loader.validate(opt)

        then = date.today() - timedelta(days=6)
        self.assertEqual(opt.date, then)

    def test_validate_replaces_absolute_date(self) -> None:
        opt = self.loader.parse_cmdline(['list', '-d', '2023-01-16'])
        self.loader.validate(opt)
        self.assertEqual(opt.date, date(2023, 1, 16))

    def test_validate_rejects_invalid_date(self) -> None:
        opt = self.loader.parse_cmdline(['list', '-d', 'autobahn'])
        with self.assertRaises(SystemExit):
            self.loader.validate(opt)
