from enum import Enum
from pydantic import BaseModel, field_validator
from datetime import date


class BandsURLData(Enum):
    ROCK = "rock"
    ELECTRIC = "electric"
    JAZZ = "jazz"


class GenreChoices(Enum):
    ROCK = "Rock"
    ELECTRIC = "Electric"
    JAZZ = "Jazz"


class Album(BaseModel):
    title: str
    date: date


class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    album: list[Album] = []


class BandCreate(BandBase):
    @field_validator("genre")
    def create_genre_title(cls, value):
        return value


class BandWithID(BandBase):
    id: int
