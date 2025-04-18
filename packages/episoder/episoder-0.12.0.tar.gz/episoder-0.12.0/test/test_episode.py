# episoder, https://code.ott.net/episoder
# -*- coding: utf8 -*-
#
# Copyright (C) 2004-2024 Stefan Ott. All rights reserved.
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

from episoder.database import Episode, Show


class TestEpisode(TestCase):

    def test_construct(self):

        episode = Episode("First", 3, 8, date(2017, 1, 1), "0XOR", 117)

        self.assertEqual(episode.show_id, None)
        self.assertEqual(episode.episode, 8)
        self.assertEqual(episode.airdate, date(2017, 1, 1))
        self.assertEqual(episode.season, 3)
        self.assertEqual(episode.title, "First")
        self.assertEqual(episode.totalnum, 117)
        self.assertEqual(episode.prodnum, "0XOR")

    def test_str_and_repr(self):

        show = Show("TvShow", "")
        episode = Episode("First", 1, 1, date(2017, 1, 1), "http://", 1)
        episode.show = show

        self.assertEqual(str(episode), "TvShow 1x01: First")
        self.assertEqual(repr(episode), 'Episode("First", 1, 1, '
                         'date(2017, 1, 1), "http://", 1)')

    def test_equality(self):

        ep1 = Episode("First", 1, 1, date(2017, 1, 1), "http://", 1)
        ep1.show_id = 1

        ep2 = Episode("Second", 2, 2, date(2017, 1, 1), "http://", 1)
        ep2.show_id = 2

        self.assertNotEqual(ep1, ep2)

        ep1.show_id = 2
        self.assertNotEqual(ep1, ep2)

        ep1.season = 2
        self.assertNotEqual(ep1, ep2)

        ep1.episode = 2
        self.assertEqual(ep1, ep2)

        ep1.season = 1
        self.assertNotEqual(ep1, ep2)

        ep1.season = 2
        ep1.show_id = 1
        self.assertNotEqual(ep1, ep2)

    def test_sorting(self):

        ep1 = Episode("A", 1, 1, date(2017, 1, 1), "", 1)
        ep2 = Episode("D", 2, 2, date(2017, 1, 1), "", 1)
        ep3 = Episode("E", 3, 1, date(2017, 1, 1), "", 1)
        ep4 = Episode("B", 1, 2, date(2017, 1, 1), "", 1)
        ep5 = Episode("C", 2, 1, date(2017, 1, 1), "", 1)

        episodes = sorted([ep1, ep2, ep3, ep4, ep5])
        self.assertEqual(episodes, [ep1, ep4, ep5, ep2, ep3])
