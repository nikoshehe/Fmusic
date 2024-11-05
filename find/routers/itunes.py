# routers/itunes.py
from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

@router.get("/itunes-search")
async def search_itunes(song: str):
    if not song:
        raise HTTPException(status_code=400, detail="No song name provided")

    url = f"https://itunes.apple.com/search?term={song}&media=music&limit=5"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from iTunes.")
    
    # Parsování odpovědi
    data = response.json()
    results = []

    for item in data.get("results", []):
        # Zajištění, že klíče existují
        track_info = {
            "song_name": item.get("trackName", "Unknown Track"),
            "artist": item.get("artistName", "Unknown Artist"),
            "url": item.get("trackViewUrl", "")
        }
        results.append(track_info)

    return {"itunes_results": results}
