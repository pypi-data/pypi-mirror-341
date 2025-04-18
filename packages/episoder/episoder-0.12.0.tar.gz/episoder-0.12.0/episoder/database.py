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

from datetime import datetime

from sqlalchemy import Column, Integer, Text, Date, ForeignKey, Sequence
from sqlalchemy import DateTime, Boolean
from sqlalchemy.orm import backref, declarative_base, relationship

Base = declarative_base()


class Show(Base):

    RUNNING = 1
    SUSPENDED = 2
    ENDED = 3

    __tablename__ = "shows"

    id = Column("show_id", Integer, Sequence("shows_show_id_seq"),
                primary_key=True)
    name = Column("show_name", Text)
    url = Column(Text, unique=True)
    updated = Column(DateTime)
    enabled = Column(Boolean)
    status = Column(Integer, default=RUNNING)

    def __init__(self, name, url="", updated=datetime.fromtimestamp(0)):

        self.name = name
        self.url = url
        self.updated = updated
        self.status = Show.RUNNING
        self.episodes = []
        self.enabled = True

    def __str__(self):

        return f"Show: {self.name}"

    def __repr__(self):

        return f'Show("{self.name}", "{self.url}")'

    def __eq__(self, other):

        return self.name == other.name and self.url == other.url


# pylint: disable=too-many-instance-attributes
class Episode(Base):

    __tablename__ = "episodes"

    show_id = Column(Integer, ForeignKey(Show.id), primary_key=True)
    episode = Column("num", Integer, primary_key=True)
    airdate = Column(Date)
    season = Column(Integer, primary_key=True)
    title = Column(Text)
    totalnum = Column(Integer)
    prodnum = Column(Text)
    notified = Column(Date)
    show = relationship(Show, backref=backref("episodes", cascade="all"))

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, name, season, episode, aired, prodnum, total):

        self.title = name
        self.season = int(season)
        self.episode = int(episode)
        self.airdate = aired
        self.prodnum = prodnum
        self.totalnum = int(total)

    def __lt__(self, other):

        return ((self.season < other.season)
                or ((self.season == other.season)
                    and (self.episode < other.episode)))

    def __str__(self):

        return f"{self.show.name} {self.season}x{self.episode:02d}: " \
                f"{self.title}"

    def __repr__(self):

        airdate = self.airdate

        return f'Episode("{self.title}", {self.season}, {self.episode}, ' \
               f'date({airdate.year}, {airdate.month}, {airdate.day}), ' \
               f'"{self.prodnum}", {self.totalnum})'

    def __eq__(self, other):

        return (self.show_id == other.show_id
                and self.season == other.season
                and self.episode == other.episode)


class Meta(Base):

    __tablename__ = "meta"
    key = Column(Text, primary_key=True)
    value = Column(Text)

    def __str__(self):

        return f"Meta: {self.key} = {self.value}"

    def __repr__(self):

        return str(self)
