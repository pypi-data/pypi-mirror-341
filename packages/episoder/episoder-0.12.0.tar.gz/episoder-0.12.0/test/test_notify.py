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

from datetime import date
from unittest import TestCase
from unittest.mock import patch, MagicMock

from episoder.database import Show, Episode
from episoder.output import EmailNotifier, NewEpisodesNotification
from episoder.output import SmtpTestMessage


class TestNotification(TestCase):
    def setUp(self) -> None:
        self.show = Show("Test show 36")

        then = date(2008, 1, 1)
        self.episode = Episode("Episode 41", 2, 5, then, "NX01", 3)
        self.episode.show = self.show

    def test_str(self) -> None:
        columbo = Show("Columbo", "")
        ep1 = Episode("Episode 1", 1, 1, date(2014, 8, 10), "x", 1)
        ep2 = Episode("Episode 2", 1, 2, date(2014, 12, 1), "x", 2)
        ep1.show = columbo
        ep2.show = columbo

        message = NewEpisodesNotification([], "%eptitle", "")
        self.assertTrue('Your upcoming episodes' in str(message))

        message = NewEpisodesNotification([ep1], "%eptitle", "")
        self.assertTrue('Your upcoming episodes' in str(message))
        self.assertTrue('Episode 1' in str(message))

        message = NewEpisodesNotification([ep1, ep2], "%eptitle", "")
        self.assertTrue('Your upcoming episodes' in str(message))
        self.assertTrue('Episode 1' in str(message))
        self.assertTrue('Episode 2' in str(message))

    def _get_test_message(self) -> NewEpisodesNotification:
        columbo = Show("Columbo", "")
        ep1 = Episode("Episode 1", 1, 1, date(2014, 8, 10), "x", 1)
        ep2 = Episode("Episode 2", 1, 2, date(2014, 12, 1), "x", 2)
        ep1.show = columbo
        ep2.show = columbo

        return NewEpisodesNotification([ep1, ep2],
                                       "[%airdate] %show %seasonx%epnum - "
                                       "%eptitle", "%Y-%m-%d")

    @patch('episoder.output.SMTP')
    def test_send_mail(self, mock_constructor: MagicMock) -> None:
        message = self._get_test_message()
        notifier = EmailNotifier('smtp.example.org', 94)
        notifier.send(message, 'person@example.org')

        mock_constructor.assert_called_with('smtp.example.org', 94)
        mock = mock_constructor.return_value
        mock.starttls.assert_not_called()
        mock.login.assert_not_called()
        mock.send_message.assert_called_with(message)
        mock.quit.assert_called()

        self.assertEqual(message['from'], 'person@example.org')
        self.assertEqual(message['to'], 'person@example.org')

    @patch('episoder.output.SMTP')
    def test_send_mail_tls(self, mock_constructor: MagicMock) -> None:
        message = self._get_test_message()
        notifier = EmailNotifier("localhost", 95)
        notifier.use_tls = True
        notifier.send(message, "xy@example.org")

        mock_constructor.assert_called_with('localhost', 95)
        mock = mock_constructor.return_value
        mock.starttls.assert_called()
        mock.login.assert_not_called()
        mock.send_message.assert_called_with(message)
        mock.quit.assert_called()

        self.assertEqual(message['from'], 'xy@example.org')
        self.assertEqual(message['to'], 'xy@example.org')

    @patch('episoder.output.SMTP')
    def test_send_mail_auth(self, mock_constructor: MagicMock) -> None:
        message = self._get_test_message()
        notifier = EmailNotifier('localhost', 96)
        notifier.set_credentials('someuser', 'somepass')
        notifier.send(message, 'xy@example.org')

        mock_constructor.assert_called_with('localhost', 96)
        mock = mock_constructor.return_value
        mock.starttls.assert_not_called()
        mock.login.assert_called_with('someuser', 'somepass')
        mock.send_message.assert_called_with(message)
        mock.quit.assert_called()

        self.assertEqual(message['from'], 'xy@example.org')
        self.assertEqual(message['to'], 'xy@example.org')

    @patch('episoder.output.SMTP')
    def test_send_test_message(self, mock_constructor: MagicMock) -> None:
        message = SmtpTestMessage()
        notifier = EmailNotifier('localhost', 97)
        notifier.send(message, 'me@example.com')

        mock_constructor.assert_called_with('localhost', 97)
        mock = mock_constructor.return_value
        mock.starttls.assert_not_called()
        mock.login.assert_not_called()
        mock.send_message.assert_called_with(message)
        mock.quit.assert_called()

        self.assertEqual(message['from'], 'me@example.com')
        self.assertEqual(message['to'], 'me@example.com')
