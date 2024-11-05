from fastapi import APIRouter, HTTPException
import httpx
import itunespy

router = APIRouter()

@router.get("/itunes-search")

async def search_itunes(song: str):
    if not song:
        raise HTTPException(status_code=400, detail="No song name provided")
    
    try:
        url = f"https://itunes.apple.com/search?term={song}&media=music&limit=5"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from iTunes.")

        data = response.json()
        results = []
        for item in data.get("results", []):
            track_info = {
                "song_name": item.get("trackName", "Unknown Track"),
                "artist": item.get("artistName", "Unknown Artist"),
                "url": item.get("trackViewUrl", "")
            }
            results.append(track_info)

        return results  # Mělo by vrátit seznam slovníků

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
