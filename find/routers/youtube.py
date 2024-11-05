from fastapi import APIRouter, HTTPException
import httpx
import requests
import re

router = APIRouter()

# YT API
YOUTUBE_API_KEY = "AIzaSyDbS4PnwAeBY8lRwmVVL67gYDjDW0cK_tQ"

def perse_youtube_title(title):
    parts = re.split(r" - | \|", title)
    if len(parts) >= 2:
        artist = parts[].strip()
        song_name(title.strip()

    return song_name, artist

@router.get("/youtube-search")
async def search_song(song: str):
    if not song:
        raise HTTPException(status_code=400, detail="No song name provided")

    youtube_result = await search_youtube(song)
    return {"youtube": youtube_result}

async def search_youtube(song_name: str):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={song_name}&type=video&maxResults=3&key={YOUTUBE_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error with YT API")

    data = response.json()
    print("API Response:", data)  # Výpis pro kontrolu obsahu

    results = []

   for item in data.get("items", []):
    snippet = item.get("snippet")
    if snippet:
        video_title = snippet.get("title")  # Získání názvu videa
        channel_title = snippet.get("channelTitle")  # Získání názvu kanálu (umělce)
        video_id = item["id"].get("videoId")
        
        if video_title and video_id:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # Rozdělení názvu na song_name a artist pomocí parse_youtube_title
            song_name, artist = parse_youtube_title(video_title)
            
            results.append({
                "song_name": song_name,  # Použije název skladby z funkce
                "artist": artist,        # Použije umělce z funkce
                "url": video_url
            })
    else:
        print("Snippet not found in item:", item)


    return results
