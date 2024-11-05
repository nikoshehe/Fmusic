# routers/itunes.py
from fastapi import APIRouter, HTTPException
import itunespy

router = APIRouter()

@router.get("/itunes-search")
async def search_itunes(song: str):
    if not song:
        raise HTTPException(status_code=400, detail="No song name provided")

    try:
        # Použití itunespy pro vyhledání skladeb
        results = itunespy.search(song, media='music', limit=3)

        itunes_results = []
        for item in results:
            track_info = {
                "song_name": item.track_name if item.track_name else "Unknown Track",  # Ověřujeme, že track_name existuje
                "artist": item.artist_name if item.artist_name else "Unknown Artist",  # Ověřujeme, že artist_name existuje
                "url": item.track_view_url if item.track_view_url else "",  # Ověřujeme, že track_view_url existuje
            }
            itunes_results.append(track_info)

        return {"itunes_results": itunes_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from iTunes: {str(e)}")
