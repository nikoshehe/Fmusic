import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from find.routers import youtube, spotify, soundcloud, itunes

app = FastAPI()

# Mount pro statické soubory (CSS, JavaScript, obrázky)
app.mount(
    "/static", 
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "find", "static")), 
    name="static"
)

# Nastavení šablon (Jinja2)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "find", "templates"))

# Youtube, Spotify, SoundCloud, iTunes routry
app.include_router(youtube.router)
app.include_router(spotify.router)
app.include_router(soundcloud.router)
app.include_router(itunes.router)

# Hlavní stránka vracející HTML šablonu
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, song: str = None):
    if song:
        youtube_results = await youtube.search_song(song)
        spotify_results = await spotify.search_song(song)
        # soundclout_results = await soundcloud.search_song(song)
        # itunes_results = await itunes.search_song(song)

        # spojí výsledky z různch platforem do jednoho slovníků
        results = {
            "youtube": youtube_results,
            "spotify": spotify_results,
            # "soundcloud": soundcloud_results,
            # "itunes": itunes_results,
        }
    else:
        # není zadáná žádná písnička
        results = {}

    return templates.TemplateResponse("index.html", {"request": request, "results": results})
