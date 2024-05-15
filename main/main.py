from fastapi import FastAPI, HTTPException
from schemas import Band, BandsURLData
app = FastAPI()

BANDS = [
    {"id": 1, "name": "New York times", "genre": "rock"},
    {"id": 2, "name": "New York times", "genre": "electronics"},
    {"id": 3, "name": "New York times", "genre": "jazz"},
    {"id": 4, "name": "New York times", "genre": "rock"}
]

@app.get("/bands")
def bandS(genre: BandsURLData | None = None, has_album: bool = False) -> list[Band]:
    band_list = [Band(**b) for b in BANDS]
    if genre:
        band_list = [ b for b in band_list if b.genre.lower()==genre]
    if has_album:
        band_list = [b for b in band_list if len(b.album) > 0]
    return band_list

@app.get("/band/{band_id}", status_code=200)
def read_about(band_id: int) -> Band:
    band = next((Band(**b) for b in BANDS if b["id"] == band_id), None)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    return band

@app.get('/bands/genre/{genre}')
def bnads_for_genre(genre: BandsURLData) -> dict:
    genre = next((g for g in BANDS if g['genre'].lower() == genre.value), None)
    if genre is None:
        raise HTTPException(status_code=404, details="Genre not found ")
    return genre