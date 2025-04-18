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

from abc import abstractmethod, ABC
from datetime import date, timedelta
from email.message import EmailMessage
from logging import getLogger
from smtplib import SMTP
from sys import stdout
from typing import Optional, TextIO

from .database import Episode


class EpisodeFormatter:
    # pylint: disable=too-few-public-methods
    def __init__(self, episode_format: str, date_format: str) -> None:
        self._format = episode_format
        self._date_format = date_format

    def format(self, episode: Episode) -> str:
        string = self._format

        airdate = episode.airdate.strftime(self._date_format)
        string = string.replace('%airdate', airdate)
        string = string.replace('%show', str(episode.show.name))
        string = string.replace('%season', str(episode.season))
        string = string.replace('%epnum', f'{episode.episode:02d}')
        string = string.replace('%eptitle', str(episode.title))
        string = string.replace('%totalep', str(episode.totalnum))
        string = string.replace('%prodnum', str(episode.prodnum))

        return string


class ConsoleRenderer(ABC):
    # pylint: disable=too-few-public-methods
    @abstractmethod
    def render(self, episodes: list[Episode], today: date) -> None:
        pass


class ColorfulRenderer(ConsoleRenderer):
    # pylint: disable=too-few-public-methods
    RED = '\033[31;1m'
    CYAN = '\033[36;1m'
    GREY = '\033[30;0m'
    GREEN = '\033[32;1m'
    YELLOW = '\033[33;1m'

    def __init__(self, fmt: str, datefmt: str, dest: TextIO = stdout) -> None:
        self._dest = dest
        self._formatter = EpisodeFormatter(fmt, datefmt)

    def _color(self, episode: Episode, yesterday: date, today: date,
               tomorrow: date) -> str:
        if episode.airdate == yesterday:
            return ColorfulRenderer.RED
        if episode.airdate == today:
            return ColorfulRenderer.YELLOW
        if episode.airdate == tomorrow:
            return ColorfulRenderer.GREEN
        if episode.airdate > tomorrow:
            return ColorfulRenderer.CYAN

        return ColorfulRenderer.GREY

    def render(self, episodes: list[Episode], today: date) -> None:
        yesterday = today - timedelta(1)
        tomorrow = today + timedelta(1)

        for episode in episodes:
            text = self._formatter.format(episode)
            color = self._color(episode, yesterday, today, tomorrow)
            self._dest.write(f'{color}{text}{ColorfulRenderer.GREY}\n')


class ColorlessRenderer(ConsoleRenderer):
    # pylint: disable=too-few-public-methods
    def __init__(self, fmt: str, datefmt: str, dest: TextIO = stdout) -> None:
        self._dest = dest
        self._formatter = EpisodeFormatter(fmt, datefmt)

    def render(self, episodes: list[Episode], _: date) -> None:
        for episode in episodes:
            text = self._formatter.format(episode)
            self._dest.write(f'{text}\n')


class EmailNotifier:
    def __init__(self, host: str, port: int) -> None:
        self._server = SMTP(host, port)
        self._user: Optional[str] = None
        self._password: Optional[str] = None

        self._log = getLogger('EmailNotifier')
        self.use_tls = False

    def __str__(self) -> str:
        return 'EmailNotifier'

    def set_credentials(self, user: str, password: str) -> None:
        self._user = user
        self._password = password

    def send(self, msg: EmailMessage, send_to: str) -> None:
        self._log.info('Sending e-mail to %s', send_to)
        msg['From'] = send_to
        msg['To'] = send_to

        if self.use_tls:
            self._server.starttls()
        if self._user and self._password:
            self._server.login(self._user, self._password)

        self._server.send_message(msg)
        self._server.quit()


class SmtpTestMessage(EmailMessage):
    def __init__(self) -> None:
        super().__init__()
        self['Subject'] = 'Test from episoder'
        self.set_content('This is a test')


class NewEpisodesNotification(EmailMessage):
    def __init__(self, episodes: list[Episode], episode_format: str,
                 date_format: str) -> None:
        super().__init__()
        self['Subject'] = 'Upcoming TV episodes'

        formatter = EpisodeFormatter(episode_format, date_format)

        body = 'Your upcoming episodes:\n\n'
        for episode in episodes:
            body += f'{formatter.format(episode)}\n'

        self.set_content(body)
