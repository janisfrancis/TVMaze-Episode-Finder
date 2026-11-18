"""List the episodes of a TV show using the free TVmaze API.

Usage:  python tvmaze_episodes.py "big bang theory"
"""
import json
import sys
import time
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://api.tvmaze.com"
CACHE_DIR = Path(".tvmaze_cache")
CACHE_TTL = 24 * 60 * 60  # seconds; episode lists rarely change


def make_session() -> requests.Session:
    """One reusable session that retries on rate limits and server errors."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,  # waits 1s, 2s, 4s between attempts
        status_forcelist=[429, 500, 502, 503, 504],
        respect_retry_after_header=True,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.headers["User-Agent"] = "episode-lister-demo/1.0"
    return session


def get_json(session: requests.Session, path: str, params: dict | None = None):
    """GET a path, with a timeout, a simple file cache and clear errors."""
    CACHE_DIR.mkdir(exist_ok=True)
    key = (path + json.dumps(params or {}, sort_keys=True)).replace("/", "_")
    cache_file = CACHE_DIR / f"{key}.json"

    if cache_file.exists() and time.time() - cache_file.stat().st_mtime < CACHE_TTL:
        return json.loads(cache_file.read_text())

    response = session.get(BASE_URL + path, params=params, timeout=10)
    if response.status_code == 404:
        raise LookupError(f"Nothing found at {path}")
    response.raise_for_status()  # any other 4xx/5xx becomes an exception

    data = response.json()
    cache_file.write_text(json.dumps(data))
    return data


def list_episodes(show_name: str) -> None:
    session = make_session()
    show = get_json(session, "/singlesearch/shows", {"q": show_name})
    episodes = get_json(session, f"/shows/{show['id']}/episodes")

    print(f"{show['name']}: {len(episodes)} episodes\n")
    for ep in episodes:
        print(f"S{ep['season']:02d}E{ep['number']:02d}  {ep['airdate']}  {ep['name']}")
    print("\nData: TVmaze.com (CC BY-SA 4.0)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: python tvmaze_episodes.py "show name"')
    try:
        list_episodes(" ".join(sys.argv[1:]))
    except (LookupError, requests.RequestException) as error:
        sys.exit(f"Could not fetch episodes: {error}")
