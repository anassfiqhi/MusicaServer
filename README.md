# MusicaServer

A Python REST API that wraps [SpotAPI](https://github.com/Aran404/SpotAPI) to expose Spotify catalog data — search, track info, albums, playlists, and a curated feed — for use by the Musica mobile app.

## Stack

| Layer | Library |
|---|---|
| Framework | FastAPI |
| Server | Hypercorn |
| Spotify access | SpotAPI (unofficial internal API) |
| Deployment | Railway (Nixpacks / Python 3) |

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/search/tracks?q=&limit=` | Search tracks (default limit 20, max 50) |
| `GET` | `/search/artists?q=&limit=` | Search artists (default limit 20, max 50) |
| `GET` | `/track/{id}` | Track metadata |
| `GET` | `/album/{id}` | Album tracks (default limit 50, max 100) |
| `GET` | `/playlist/{id}` | Playlist tracks (default limit 50, max 100) |
| `GET` | `/feed` | Curated list of featured playlist IDs + metadata |

All IDs are Spotify track/album/artist/playlist IDs (the string after the last `/` in a Spotify URL).

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy the environment file:

```bash
cp .env.example .env
```

Start the server:

```bash
hypercorn main:app --reload
```

API docs available at `http://localhost:8000/docs` (Swagger UI).

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SPOTIFY_EMAIL` | No | Spotify account email (for future authenticated endpoints) |
| `SPOTIFY_PASSWORD` | No | Spotify account password |

Public endpoints (search, track info, albums, playlists, feed) work without credentials.

## Deploy to Railway

1. Push this repo to GitHub.
2. Create a new Railway project → **Deploy from GitHub repo**.
3. Railway detects Python automatically via Nixpacks.
4. Add `SPOTIFY_EMAIL` and `SPOTIFY_PASSWORD` as environment variables if needed.

## Notes

- SpotAPI interacts with Spotify's **internal** (private) API. This is not the official Spotify Web API and violates Spotify's Terms of Service. Use for personal/development purposes only.
- The `/feed` endpoint returns a static list of stable Spotify playlist IDs. Fetch individual playlist tracks via `/playlist/{id}`.
