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

from os import environ
from os.path import basename
from unittest import TestCase

from pyfakefs.fake_filesystem_unittest import Patcher

from episoder.config import ConfigLoader, InvalidDataFormatError
from episoder.version import __version__


class TestLoadConfig(TestCase):
    def setUp(self) -> None:
        self.loader = ConfigLoader()

    def test_load_empty_config(self) -> None:
        with Patcher() as patch:
            patch.fs.create_file('/etc/episoder.ini', contents='')
            cfg = self.loader.load('/etc/episoder.ini')

        self.assertTrue(len(__version__) > 3)
        self.assertEqual(cfg.agent, 'episoder/' + __version__)

        self.assertTrue(cfg.datafile.startswith(environ['HOME']))
        self.assertEqual(basename(cfg.datafile), '.episodes')
        self.assertEqual(cfg.dateformat, '%a, %b %d, %Y')
        self.assertEqual(cfg.format, '%airdate %show %seasonx%epnum')
        self.assertEqual(cfg.tvdb_key, '8F15287C4B23B36E')

        self.assertEqual(cfg.email_to, None)
        self.assertEqual(cfg.email_username, None)
        self.assertEqual(cfg.email_password, None)
        self.assertEqual(cfg.email_server, 'localhost')
        self.assertEqual(cfg.email_port, 587)
        self.assertEqual(cfg.email_tls, False)

    def test_load_data_file_path_from_config(self) -> None:
        with Patcher() as patch:
            patch.fs.create_file('/usr/local/episoder.ini',
                                 contents='data=/opt/episodes.db')
            cfg = self.loader.load('/usr/local/episoder.ini')

        self.assertEqual(cfg.datafile, '/opt/episodes.db')

    def test_load_date_format_from_config(self) -> None:
        with Patcher() as patch:
            patch.fs.create_file('/usr/local/episoder.ini',
                                 contents='dateformat=%m in %Y')
            cfg = self.loader.load('/usr/local/episoder.ini')

        self.assertEqual(cfg.dateformat, '%m in %Y')

    def test_load_format_from_config(self) -> None:
        with Patcher() as patch:
            patch.fs.create_file('/etc/episoder.ini',
                                 contents='format=%show %eptitle')
            cfg = self.loader.load('/etc/episoder.ini')

        self.assertEqual(cfg.format, '%show %eptitle')

    def test_load_user_agent_from_config(self) -> None:
        with Patcher() as patch:
            patch.fs.create_file('/mnt/config/episoder.ini',
                                 contents='agent=Mozilla/4.0')
            cfg = self.loader.load('/mnt/config/episoder.ini')

        self.assertEqual(cfg.agent, 'Mozilla/4.0')

    def test_load_tvdb_key_from_config(self) -> None:
        with Patcher() as patch:
            patch.fs.create_file('/etc/episoder.ini',
                                 contents='tvdb_key=1234567')
            cfg = self.loader.load('/etc/episoder.ini')

        self.assertEqual(cfg.tvdb_key, '1234567')

    def test_load_email_settings_from_config(self) -> None:
        with Patcher() as patch:
            patch.fs.create_file('/etc/episoder.ini',
                                 contents='''
                                 email_to=me@example.net
                                 email_username=Hans
                                 email_password=s3kr1t
                                 email_server=localhost:1235
                                 email_port=255
                                 email_tls=True
                                 ''')
            cfg = self.loader.load('/etc/episoder.ini')

        self.assertEqual(cfg.email_to, 'me@example.net')
        self.assertEqual(cfg.email_username, 'Hans')
        self.assertEqual(cfg.email_password, 's3kr1t')
        self.assertEqual(cfg.email_port, 255)
        self.assertEqual(cfg.email_server, 'localhost:1235')
        self.assertEqual(cfg.email_tls, True)

    def test_validate_config_with_data_file_that_does_not_exist(self) -> None:
        with Patcher() as patch:
            patch.fs.create_file('/usr/local/episoder.ini',
                                 contents='data=/opt/episodes.db')
            cfg = self.loader.load('/usr/local/episoder.ini')
            self.loader.validate(cfg)

    def test_validate_config_with_invalid_data_file(self) -> None:
        with Patcher() as patch:
            patch.fs.create_file('/usr/local/episoder.ini',
                                 contents='data=/opt/episodes.db')
            patch.fs.create_file('/opt/episodes.db', contents='hello')
            cfg = self.loader.load('/usr/local/episoder.ini')
            with self.assertRaises(InvalidDataFormatError):
                self.loader.validate(cfg)

    def test_validate_config_with_valid_data_file(self) -> None:
        with Patcher() as patch:
            patch.fs.create_file('/usr/local/episoder.ini',
                                 contents='data=/opt/episodes.db')
            patch.fs.create_file('/opt/episodes.db', contents='SQLite')
            cfg = self.loader.load('/usr/local/episoder.ini')
            self.loader.validate(cfg)
