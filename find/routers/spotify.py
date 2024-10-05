from fastapi import APIRouter, HTTPException
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import os

router = APIRouter()

SPOTIPY_CLIENT_ID = ("b3a4d3cfad2a47b0a224ced21d677cc1")
SPOTIPY_CLIENT_SECRET = ("6227f257990549d39584351486e05f5a")

# Nastavení Spotify API klienta s autentizací
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = Spotify(auth_manager=auth_manager)

@router.get("/spotify=search")
async def search_spotify(song: str):
    if not song:
        raise HTTPException(status_code=400, detail = "No song name provided")

    try:
        results = sp.search(q=song, limit=5, type='track')
        tracks = results['tracks']["items"]

        response = []
        for track in tracks:
            track_info = {
                "song_name": track['name'],
                "artist": track['artists'][0]['name'],
                "url": track['extermal_urls']['spotify']
            }
            response.append(track_info)

        return {"spotify_results": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error accessing Spotify API: {str(e)}")
