from enum import Enum
from pydantic import BaseModel
from datetime import date

class BandsURLData(Enum):
    ROCK = 'rock'
    ELECTRIC = 'electric'
    JAZZ = 'jazz'
    

class Album(BaseModel):
    title: str
    date: date

class Band(BaseModel):
    id : int
    name: str
    genre: str
    album: Album