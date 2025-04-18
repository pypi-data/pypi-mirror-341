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

import logging
from datetime import date, timedelta
from typing import Optional

import sqlite3
from sqlalchemy import create_engine, or_, and_, select, inspect
from sqlalchemy.orm import sessionmaker

from .database import Episode, Show, Meta


class Database:
    def __init__(self, path: str) -> None:
        self._path = path
        self.logger = logging.getLogger('Database')

        self.open()
        self._initdb()

    def __str__(self) -> str:
        return f'Episoder Database at {self._path}'

    def __repr__(self) -> str:
        return f'Database({self._path})'

    def _initdb(self) -> None:
        inspector = inspect(self.engine)

        # Initialize the database if all tables are missing
        names = [Show, Episode, Meta]
        tables = [t for t in names if inspector.has_table(t.__table__.name)]

        if len(tables) < 1:
            Show.__table__.create(bind=self.engine)
            Episode.__table__.create(bind=self.engine)
            Meta.__table__.create(bind=self.engine)
            self.set_schema_version(4)

    def open(self) -> None:
        if self._path.find('://') > -1:
            self.engine = create_engine(self._path)
        else:
            self.engine = create_engine(f'sqlite:///{self._path}')

        session = sessionmaker(self.engine)
        self.session = session()
        self.session.begin()

    def close(self) -> None:
        self.session.commit()
        self.session.close()
        self.engine.dispose()

    def set_schema_version(self, version: int) -> None:
        meta = Meta()
        meta.key = 'schema'
        meta.value = f'{version}'

        with self.session.begin_nested():
            self.session.merge(meta)

    def get_schema_version(self) -> int:
        inspector = inspect(self.engine)
        if not inspector.has_table(Meta.__table__.name):
            return 1

        res = self.session.scalars(
                select(Meta).where(Meta.key == "schema")).first()
        if res:
            return int(res.value)

        return 0

    def clear(self) -> None:
        episodes = self.session.query(Episode).all()

        for episode in episodes:
            self.session.delete(episode)

        self.session.flush()

    def migrate(self) -> None:
        schema_version = self.get_schema_version()
        self.logger.debug("Found schema version %s", schema_version)

        if schema_version < 0:
            self.logger.debug("Automatic schema updates disabled")
            return

        if schema_version == 1:
            # Upgrades from version 1 are rather harsh, we
            # simply drop and re-create the tables
            self.logger.debug("Upgrading to schema version 2")

            upgrade = sqlite3.connect(self._path)
            upgrade.execute("DROP TABLE episodes")
            upgrade.execute("DROP TABLE shows")
            upgrade.close()

            Show.__table__.create(bind=self.engine)
            Episode.__table__.create(bind=self.engine)
            Meta.__table__.create(bind=self.engine)

            schema_version = 4
            self.set_schema_version(schema_version)

        if schema_version == 2:
            # Add two new columns to the shows table
            self.logger.debug("Upgrading to schema version 3")

            # We can only do this with sqlite databases
            assert self.engine.driver == "pysqlite"

            self.close()

            upgrade = sqlite3.connect(self._path)
            upgrade.execute("ALTER TABLE shows "
                            "ADD COLUMN enabled TYPE boolean")
            upgrade.execute("ALTER TABLE shows "
                            "ADD COLUMN status TYPE integer")
            upgrade.close()

            self.open()
            schema_version = 3
            self.set_schema_version(schema_version)

        if schema_version == 3:
            # Add a new column to the episodes table
            self.logger.debug("Upgrading to schema version 4")

            # We can only do this with sqlite databases
            assert self.engine.driver == "pysqlite"

            self.close()

            upgrade = sqlite3.connect(self._path)
            upgrade.execute("ALTER TABLE episodes "
                            "ADD COLUMN notified TYPE date")
            upgrade.close()

            self.open()
            schema_version = 4
            self.set_schema_version(schema_version)

    def get_expired_shows(self, today: date = date.today()) -> list[Show]:
        delta_running = timedelta(2)    # 2 days
        delta_suspended = timedelta(7)    # 1 week
        delta_ended = timedelta(14)    # 2 weeks

        shows = self.session.query(Show).filter(or_(
                and_(
                    Show.enabled,
                    Show.status == Show.RUNNING,
                    Show.updated < today - delta_running
                ),
                and_(
                    Show.enabled,
                    Show.status == Show.SUSPENDED,
                    Show.updated < today - delta_suspended
                ),
                and_(
                    Show.enabled,
                    Show.status == Show.ENDED,
                    Show.updated < today - delta_ended
                )
        ))

        return shows.all()

    def get_enabled_shows(self) -> list[Show]:
        shows = self.session.query(Show).filter(Show.enabled)
        return shows.all()

    def get_show_by_url(self, url: str) -> Optional[Show]:
        shows = self.session.query(Show).filter(Show.url == url)

        if shows.count() < 1:
            return None

        return shows.first()

    def get_show_by_id(self, show_id: int) -> Optional[Show]:
        return self.session.scalars(
                select(Show).where(Show.id == show_id)).first()

    def add_show(self, show: Show) -> Show:
        show = self.session.merge(show)
        self.session.flush()
        return show

    def remove_show(self, show: Show) -> None:
        assert show is not None
        episodes = self.session.scalars(select(Episode))

        hits = [e for e in episodes if e.show_id == show.id]
        for episode in hits:
            self.session.delete(episode)

        self.session.delete(show)
        self.session.flush()

    def get_shows(self) -> list[Show]:
        return self.session.query(Show).all()

    def add_episode(self, episode: Episode, show: Show) -> None:
        episode.show_id = show.id
        self.session.merge(episode)
        self.session.flush()

    def get_episodes(self, basedate: date = date.today(),
                     days: int = 0) -> list[Episode]:
        enddate = basedate + timedelta(days)

        return self.session.query(Episode). \
            filter(Episode.airdate >= basedate). \
            filter(Episode.airdate <= enddate). \
            order_by(Episode.airdate).all()

    def search(self, term: str) -> list[Episode]:
        query = self.session.query(Episode).join(Episode.show)
        return query.filter(or_(
                Episode.title.like(f"%%{term}%%"),
                Show.name.like(f"%%{term}%%"))). \
            order_by(Episode.airdate.asc()).all()

    def commit(self) -> None:
        self.session.commit()
        self.session.begin()

    def rollback(self) -> None:
        self.session.rollback()
        self.session.begin()

    def remove_before(self, then: date, show: Optional[Show] = None) -> None:
        logging.debug("Removing episodes from before %s", then)
        episodes = self.session.query(Episode).filter(Episode.airdate < then)

        if show:
            episodes = episodes.filter(Episode.show == show)

        for episode in episodes:
            self.session.delete(episode)

        self.commit()
