import itertools
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from spotapi import Public
from spotapi.exceptions import AlbumError, ArtistError, SongError

load_dotenv()

app = FastAPI(title="MusicaServer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok", "service": "MusicaServer"}


# ── Search ────────────────────────────────────────────────────────────────────

@app.get("/search/tracks")
def search_tracks(
    q: str,
    limit: int = Query(20, ge=1, le=50),
):
    try:
        results = list(itertools.islice(Public.song_search(q), limit))
        return {"tracks": results, "total": len(results)}
    except SongError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/artists")
def search_artists(
    q: str,
    limit: int = Query(20, ge=1, le=50),
):
    try:
        results = list(itertools.islice(Public.artist_search(q), limit))
        return {"artists": results, "total": len(results)}
    except ArtistError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Tracks ────────────────────────────────────────────────────────────────────

@app.get("/track/{track_id}")
def get_track(track_id: str):
    try:
        return Public.song_info(track_id)
    except SongError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Albums ────────────────────────────────────────────────────────────────────

@app.get("/album/{album_id}")
def get_album(
    album_id: str,
    limit: int = Query(50, ge=1, le=100),
):
    try:
        tracks = list(itertools.islice(Public.album_info(album_id), limit))
        return {"tracks": tracks, "total": len(tracks)}
    except AlbumError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Playlists ─────────────────────────────────────────────────────────────────

@app.get("/playlist/{playlist_id}")
def get_playlist(
    playlist_id: str,
    limit: int = Query(50, ge=1, le=100),
):
    try:
        tracks = list(itertools.islice(Public.playlist_info(playlist_id), limit))
        return {"tracks": tracks, "total": len(tracks)}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


# ── Feed ──────────────────────────────────────────────────────────────────────

FEED_SECTIONS = [
    {
        "title": "Global Top 50",
        "playlist_id": "37i9dQZEVXbMDoHDwVN2tF",
        "cover": "https://charts-images.scdn.co/assets/regionclients/global/primary/default.jpg",
    },
    {
        "title": "Today's Top Hits",
        "playlist_id": "37i9dQZF1DXcBWIGoYBM5M",
        "cover": "https://i.scdn.co/image/ab67706f000000027ea4d505212b9de1f72b5f4b",
    },
    {
        "title": "New Music Friday",
        "playlist_id": "37i9dQZF1DX4JAvHpjipBk",
        "cover": "https://i.scdn.co/image/ab67706f00000002b34cb31be6e81f5e9f9abff7",
    },
    {
        "title": "Hot Hits USA",
        "playlist_id": "37i9dQZEVXbLiRSasKsNU9",
        "cover": "https://i.scdn.co/image/ab67706f000000023b8bcd87f2873e76d9e2f5e2",
    },
    {
        "title": "Viral 50 Global",
        "playlist_id": "37i9dQZEVXbG9PaY9ysBUa",
        "cover": "https://charts-images.scdn.co/assets/regionclients/global/viral/default.jpg",
    },
]


@app.get("/feed")
def get_feed():
    return {"sections": FEED_SECTIONS}
