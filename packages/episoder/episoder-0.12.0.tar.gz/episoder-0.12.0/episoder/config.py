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

from logging import getLogger
from os import environ, path

from typing import BinaryIO, Optional

from .version import __version__


class InvalidDataFormatError(Exception):
    def __init__(self, filename: str) -> None:
        super().__init__(f'Please remove old/invalid data file: {filename}')


class EpisoderConfig:
    # pylint: disable=too-few-public-methods,too-many-instance-attributes
    def __init__(self) -> None:
        self.agent = f'episoder/{__version__}'
        self.datafile = path.join(environ['HOME'], '.episodes')
        self.dateformat = '%a, %b %d, %Y'
        self.format = '%airdate %show %seasonx%epnum'
        self.tvdb_key = '8F15287C4B23B36E'

        self.email_to: Optional[str] = None
        self.email_username: Optional[str] = None
        self.email_password: Optional[str] = None
        self.email_server = 'localhost'
        self.email_port = 587
        self.email_tls = False


class ConfigLoader:
    def __init__(self) -> None:
        self._log = getLogger('Config')

    def _load_rcfile(self, file_: BinaryIO) -> dict[str, str]:
        def strip_comments(line: str) -> str:
            return line.split('#')[0]

        def valid(line: str) -> bool:
            return '=' in line

        self._log.info('Loading config file')
        lines = file_.readlines()
        decoded_lines = [x.decode('utf8').strip() for x in lines]
        non_comments = map(strip_comments, decoded_lines)
        valid_lines = filter(valid, non_comments)
        return dict(line.split('=') for line in valid_lines)

    def _update(self, cfg: EpisoderConfig, values: dict[str, str]) -> None:
        cfg.agent = values.get('agent', cfg.agent)
        cfg.datafile = values.get('data', cfg.datafile)
        cfg.dateformat = values.get('dateformat', cfg.dateformat)
        cfg.format = values.get('format', cfg.format)
        cfg.tvdb_key = values.get('tvdb_key', cfg.tvdb_key)

        cfg.email_to = values.get('email_to', cfg.email_to)
        cfg.email_username = values.get('email_username', cfg.email_username)
        cfg.email_password = values.get('email_password', cfg.email_password)
        cfg.email_port = int(values.get('email_port', cfg.email_port))
        cfg.email_server = values.get('email_server', cfg.email_server)
        cfg.email_tls = bool(values.get('email_tls', cfg.email_tls))

    def load(self, file: str) -> EpisoderConfig:
        config = EpisoderConfig()

        if path.exists(file):
            with open(file, 'rb') as file_:
                values = self._load_rcfile(file_)

            self._log.debug('Settings loaded: %s', values)
            self._update(config, values)
            self._log.info("Loaded configuration")
        else:
            self._log.warning('No config file found, using defaults')

        return config

    def validate(self, config: EpisoderConfig) -> None:
        filename = config.datafile
        if path.exists(filename):
            with open(filename, 'rb') as file:
                data = file.read(6)

            if data != b'SQLite':
                raise InvalidDataFormatError(filename)
