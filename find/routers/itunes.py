# routers/itunes.py
from fastapi import APIRouter, HTTPException
import itunespy

router = APIRouter()

@router.get("/itunes-search")
async def search_itunes(song: str):
    if not song:
        raise HTTPException(status_code=400, detail="No song name provided")

    # Vytvoření instance Itunes
    itunes = Itunes()

    try:
        # Vyhledávání skladeb
        results = itunes.search(song, media='music', limit=5)

        # Zpracování výsledků
        itunes_results = []
        for item in results:
            track_info = {
                "song_name": item.track_name,  # Uprav na skutečné atributy
                "artist": item.artist_name,
                "url": item.track_view_url,
            }
            itunes_results.append(track_info)

        return {"itunes_results": itunes_results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from iTunes: {str(e)}")
