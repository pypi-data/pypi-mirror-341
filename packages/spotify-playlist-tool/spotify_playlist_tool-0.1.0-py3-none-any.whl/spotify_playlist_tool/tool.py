
import json
import argparse
import os
import sys
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CONFIG_PATH = os.path.expanduser("~/.spotify_config.json")

def get_spotify_client():
    if not os.path.exists(CONFIG_PATH):
        dummy_config = {
            "client_id": "your-client-id-here",
            "client_secret": "your-client-secret-here",
            "redirect_uri": "http://127.0.0.1:8888/callback"
        }
        with open(CONFIG_PATH, "w") as f:
            json.dump(dummy_config, f, indent=2)
        print(f"A config file has been created at {CONFIG_PATH}. Please update it.")
        exit(1)

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        redirect_uri=config["redirect_uri"],
        scope="user-library-read playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative"
    ))

def is_file(path):
    return os.path.isfile(path)

def get_playlist_id_by_name(sp, name, create_if_missing=False):
    user_id = sp.me()["id"]
    playlists = sp.current_user_playlists(limit=50)
    for playlist in playlists["items"]:
        if playlist["name"].lower() == name.lower():
            return playlist["id"]
    if create_if_missing:
        print(f"Creating new playlist: {name}")
        new_playlist = sp.user_playlist_create(user=user_id, name=name, public=True)
        return new_playlist["id"]
    else:
        print(f"Playlist named '{name}' not found.")
        exit(1)

def fetch_tracks_from_spotify(sp, source):
    print(f"Fetching from playlist: {source}")
    if source.lower() == "liked":
        results = sp.current_user_saved_tracks(limit=50)
        tracks = []
        while results:
            for item in results["items"]:
                if item["track"]:
                    tracks.append(item["track"])
            if results["next"]:
                results = sp.next(results)
            else:
                break
        return tracks
    else:
        results = sp.playlist_items(source, limit=100)
        tracks = []
        while results:
            for item in results["items"]:
                if item["track"]:
                    tracks.append(item["track"])
            if results["next"]:
                results = sp.next(results)
            else:
                break
        return tracks

def fetch_audio_features(sp, tracks):
    ids = [t["id"] for t in tracks if t.get("id")]
    feature_map = {}
    for i in range(0, len(ids), 100):
        audio_feats = sp.audio_features(ids[i:i+100])
        for feat in audio_feats:
            if feat:
                feature_map[feat["id"]] = feat
    return feature_map

def filter_tracks(tracks, filters, feature_map=None):
    def match(t):
        if "artist" in filters and filters["artist"].lower() not in [a["name"].lower() for a in t["artists"]]:
            return False
        if "after" in filters and t["album"]["release_date"] < filters["after"]:
            return False
        if "before" in filters and t["album"]["release_date"] > filters["before"]:
            return False
        af = feature_map.get(t["id"]) if feature_map else {}
        for key, op, val in [
            ("tempo", "min_tempo", ">="),
            ("tempo", "max_tempo", "<="),
            ("energy", "min_energy", ">="),
            ("energy", "max_energy", "<="),
            ("valence", "min_valence", ">="),
            ("valence", "max_valence", "<="),
            ("danceability", "min_dance", ">="),
            ("danceability", "max_dance", "<="),
        ]:
            fkey = op
            if fkey in filters and af:
                if op.startswith("min") and af.get(key, 0) < filters[fkey]:
                    return False
                if op.startswith("max") and af.get(key, 0) > filters[fkey]:
                    return False
        return True
    return [t for t in tracks if match(t)]

def deduplicate(tracks):
    seen = set()
    result = []
    for t in tracks:
        if t["id"] and t["id"] not in seen:
            seen.add(t["id"])
            result.append(t)
    return result

def sort_tracks(tracks, method):
    if method == "alpha":
        return sorted(tracks, key=lambda t: t["name"].lower())
    elif method == "artist":
        return sorted(tracks, key=lambda t: t["artists"][0]["name"].lower())
    elif method == "date":
        return sorted(tracks, key=lambda t: t["album"]["release_date"])
    return tracks

def save_tracks_to_file(tracks, path):
    with open(path, "w") as f:
        json.dump(tracks, f, indent=2)
    print(f"Saved {len(tracks)} tracks to {path}")

def load_tracks_from_file(path):
    with open(path) as f:
        return json.load(f)

def push_tracks_to_playlist(sp, playlist_id, tracks, nodup=False):
    uris = [t["uri"] for t in tracks if "uri" in t]
    if nodup:
        existing = fetch_tracks_from_spotify(sp, playlist_id)
        existing_uris = {t["uri"] for t in existing}
        original_len = len(uris)
        uris = [uri for uri in uris if uri not in existing_uris]
        if not uris:
            print(f"All {original_len} tracks already exist in the destination playlist. No new tracks added.")
            return
    print(f"Adding {len(uris)} tracks to playlist...")
    for i in range(0, len(uris), 100):
        sp.playlist_add_items(playlist_id, uris[i:i+100])
    print("Done.")

def main():
    parser = argparse.ArgumentParser(description="Spotify Playlist Tool (Final + Fixes)")
    parser.add_argument("--source", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--nodup", action="store_true")
    parser.add_argument("--sort", choices=["alpha", "artist", "date"])
    parser.add_argument("--random", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--after")
    parser.add_argument("--before")
    parser.add_argument("--artist")
    parser.add_argument("--min_tempo", type=float)
    parser.add_argument("--max_tempo", type=float)
    parser.add_argument("--min_energy", type=float)
    parser.add_argument("--max_energy", type=float)
    parser.add_argument("--min_valence", type=float)
    parser.add_argument("--max_valence", type=float)
    parser.add_argument("--min_dance", type=float)
    parser.add_argument("--max_dance", type=float)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    sp = get_spotify_client()

    filters = {k: v for k, v in vars(args).items() if v is not None and k.startswith(("min_", "max_", "after", "before", "artist"))}

    # Resolve playlist names
    src = args.source
    dst = args.dest
    if not is_file(src) and src.lower() not in ["liked"] and len(src) != 22:
        src = get_playlist_id_by_name(sp, src)
    if not is_file(dst) and dst.lower() not in ["liked"] and len(dst) != 22:
        dst = get_playlist_id_by_name(sp, dst, create_if_missing=True)

    if src == dst and not args.force:
        print("Error: source and destination are the same. Use --force to override.")
        sys.exit(1)

    # Load tracks
    if is_file(args.source):
        print(f"Reading source from file: {args.source}")
        tracks = load_tracks_from_file(args.source)
    else:
        tracks = fetch_tracks_from_spotify(sp, src)

    tracks = deduplicate(tracks)

    if filters:
        feature_map = fetch_audio_features(sp, tracks)
        tracks = filter_tracks(tracks, filters, feature_map)

    if args.sort:
        print(f"Sorting by: {args.sort}")
        tracks = sort_tracks(tracks, args.sort)

    if args.random:
        print("Randomizing order")
        random.shuffle(tracks)

    if is_file(args.dest) or args.dest.endswith(".json"):
        save_tracks_to_file(tracks, args.dest)
    else:
        push_tracks_to_playlist(sp, dst, tracks, nodup=args.nodup)


