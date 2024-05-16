from enum import Enum
from pydantic import field_validator
from datetime import date
from sqlmodel import SQLModel, Field, Relationship


class BandsURLData(Enum):
    ROCK = "rock"
    ELECTRIC = "electric"
    JAZZ = "jazz"


class GenreChoices(Enum):
    ROCK = "Rock"
    ELECTRIC = "Electric"
    JAZZ = "Jazz"


class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int = Field(foreign_key="band.id")


class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates="album")


class BandBase(SQLModel):
    name: str
    genre: GenreChoices


class BandCreate(BandBase):
    album: list[AlbumBase] | None = None

    @field_validator("genre")
    def check_genre(cls, value):
        return value


class Band(BandBase, table=True):
    id: int = Field(primary_key=True)
    album: list[Album] = Relationship(back_populates="band")
