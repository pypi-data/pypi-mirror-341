# episoder, https://code.ott.net/episoder
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

from abc import ABC, abstractmethod

from episoder.database import Show
from episoder.episoder import Database


class Parser(ABC):
    @abstractmethod
    def accept(self, url: str) -> bool:
        """Test if this parser can load the given URL"""

    @abstractmethod
    def parse(self, show: Show, database: Database) -> None:
        """Load episodes with this parser"""
