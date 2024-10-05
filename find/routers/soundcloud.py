# routers/soundcloud.py
from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

# Získej client_id z proměnné prostředí nebo ji nastav přímo
SOUNDCLOUD_CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID", "your_client_id")  # Přidej svá data

@router.get("/soundcloud-search")
async def search_soundcloud(song: str):
    url = f"https://api.soundcloud.com/tracks?q={song}&client_id={SOUNDCLOUD_CLIENT_ID}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from SoundCloud.")
    
    return response.json()
