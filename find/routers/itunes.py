# routers/itunes.py
from fastapi import APIRouter, HTTPException
from itunespy import itunespy  # Importuj iTunesPy knihovnu

router = APIRouter()

@router.get("/itunes-search")
async def search_itunes(song: str):
    if not song:
        raise HTTPException(status_code=400, detail="No song name provided")

    # Vyhledání skladeb pomocí knihovny iTunesPy
    results = itunespy.search_itunes(song, media='music', limit=5)

    # Zpracování výsledků
    track_info_list = []
    for item in results:
        track_info = {
            "song_name": item.track_name,  # Název skladby
            "artist": item.artist_name,     # Název umělce
            "url": item.track_view_url      # URL skladby
        }
        track_info_list.append(track_info)

    return {"itunes_results": track_info_list}
