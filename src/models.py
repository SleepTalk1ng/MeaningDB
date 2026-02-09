from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base,str_an, int_an


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str_an]
    permission: Mapped[int_an]
    nickname: Mapped[str_an]
    photo: Mapped[str_an]

class Media(Base):
    title: Mapped[str_an]
    type: Mapped[str_an]
    poster_url: Mapped[str_an]
    description: Mapped[str_an]
    release_date: Mapped[datetime] = mapped_column()

class Theme(Base):
    title: Mapped[str_an]
    description: Mapped[str_an]

class Platform(Base):
    title: Mapped[str_an]
    media_id: Mapped[int_an]
    ref_link: Mapped[str_an]

class Bond(Base):
    media_id: Mapped[int_an]
    theme_id: Mapped[int_an]
    description: Mapped[str_an]
