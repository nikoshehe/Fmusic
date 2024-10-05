# routers/itunes.py
from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/itunes-search")
async def search_itunes(song: str):
    if not song:
        raise HTTPException(status_code=400, detail="No song name provided")

    url = f"https://itunes.apple.com/search?term={song}&media=music&limit=5"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from iTunes.")
    
    # Parsování odpovědi
    data = response.json()
    results = []
    
    for item in data.get("results", []):
        track_info = {
            "song_name": item["trackName"],
            "artist": item["artistName"],
            "url": item["trackViewUrl"]
        }
        results.append(track_info)

    return {"itunes_results": results}
