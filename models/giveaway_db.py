from __future__ import annotations

from pathlib import Path
from typing import Dict

from sqlalchemy import Integer, create_engine, select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session


DB_PATH = Path("giveaway.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"


# -------------------------
# Base model
# -------------------------

class Base(DeclarativeBase):
    pass


# -------------------------
# User chance model
# -------------------------

class UserChance(Base):
    """
    Stores user chances for the single active giveaway.
    """

    __tablename__ = "user_chances"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chance: Mapped[int] = mapped_column(Integer, nullable=False)


# -------------------------
# Database manager
# -------------------------
class GiveawayDB:

    def __init__(self) -> None:
        self.engine = create_engine(
            DATABASE_URL,
            echo=False,
            future=True,
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

        Base.metadata.create_all(self.engine)

    # -------------------------
    # Session helper
    # -------------------------
    def _session(self) -> Session:
        return self.SessionLocal()

    # -------------------------
    # Increment chance
    # -------------------------
    def add_chance(self, user_id: int, value: int = 1) -> None:
        """
        Safely increments user chance
        Creates user if not exists
        """

        with self._session() as session:
            user = session.get(UserChance, user_id)

            if user is None:
                user = UserChance(user_id=user_id, chance=value)
                session.add(user)
            else:
                user.chance += value

            session.commit()

    # -------------------------
    # Set exact chance
    # -------------------------
    def set_chance(self, user_id: int, value: int) -> None:
        """
        Sets exact chance value
        """

        with self._session() as session:
            user = session.get(UserChance, user_id)

            if user is None:
                session.add(UserChance(user_id=user_id, chance=value))
            else:
                user.chance = value

            session.commit()

    # -------------------------
    # Remove user
    # -------------------------
    def remove_user(self, user_id: int) -> None:
        """
        Deletes user from giveaway
        """

        with self._session() as session:
            user = session.get(UserChance, user_id)

            if user:
                session.delete(user)
                session.commit()

    # -------------------------
    # Clear giveaway table
    # -------------------------
    def clear(self) -> None:
        """
        Removes all users
        """

        with self._session() as session:
            session.execute(delete(UserChance))
            session.commit()

    # -------------------------
    # Get all users in optimal format
    # -------------------------
    def get_all(self) -> Dict[int, int]:
        """
        Returns `{user_id: chance}`
        """

        with self._session() as session:
            stmt = select(UserChance.user_id, UserChance.chance)
            rows = session.execute(stmt).all()

            return {user_id: chance for user_id, chance in rows}