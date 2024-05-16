from fastapi import Depends, FastAPI, HTTPException, Query
from models import BandBase, BandsURLData, BandCreate, Band, Album
from typing import Annotated
from sqlmodel import Session, select
from db import create_db, get_session
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db()
        yield
    except Exception as e:
        raise e


app = FastAPI(lifespan=lifespan)


@app.get("/bands")
def bandS(
    genre: BandsURLData | None = None,
    q: Annotated[str, Query(max_length=50)] = None,
    session: Session = Depends(get_session),
) -> list[Band]:
    band_list = session.exec(select(Band)).all()
    if genre:
        band_list = [b for b in band_list if b.genre.lower() == genre]
    if q:
        band_list = [b for b in band_list if q.lower() in b.name.lower()]
    return band_list


@app.get("/band/{band_id}", status_code=200)
def read_about(band_id: int, session: Session = Depends(get_session)) -> Band:
    band = session.get(Band, band_id)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    return band


# @app.get("/bands/genre/{genre}")
# def bnads_for_genre(
#     genre: BandsURLData, session: Session = Depends(get_session)
# ) -> dict:
#     genre = session.get(Band, {"genre": genre}).id
#     if genre is None:
#         raise HTTPException(status_code=404, details="Genre not found ")
#     return genre


@app.post("/bands")
def bands(band_data: BandCreate, session: Session = Depends(get_session)) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)
    if band_data.album:
        for album in band_data.album:
            album = Album(
                title=album.title, release_date=album.release_date, band_id=band.id
            )
            session.add(album)
            session.commit()
            session.refresh(album)

    session.commit()
    session.refresh(band)
    return band
