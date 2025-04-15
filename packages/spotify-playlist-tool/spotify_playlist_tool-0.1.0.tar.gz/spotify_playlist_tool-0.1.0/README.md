# Spotify Playlist Tool

A command-line interface (CLI) for managing and filtering Spotify playlists using the Spotify Web API. Export to JSON, filter by artist or mood, randomize tracks, and avoid duplicates—all with a single command.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- Export from or import to JSON
- Filter by:
  - Artist name
  - Release date (`--after`, `--before`)
  - Audio features: tempo, energy, valence, danceability
- Shuffle or sort tracks
- Avoid re-adding duplicates
- Resolves playlist names (auto-creates if not found)
- Safety protection with `--force`

## Installation

Clone the repository and install with pip:

```bash
git clone https://github.com/gretchycat/spotify_playlist_tool.git
cd spotify_playlist_tool
pip install .
```

## Usage

```bash
spotify_playlist_tool --source liked --dest "My Mood Booster" --random --min_valence 0.6 --nodup
```

## Command-line Options

- `--source`  — Spotify playlist ID, name, `liked`, or a local JSON file
- `--dest`    — Playlist ID, name, or JSON file
- `--artist`  — Filter by artist name
- `--after` / `--before` — Filter by release date (YYYY-MM-DD)
- `--min_tempo`, `--max_energy`, `--min_valence`, etc. — Filter by audio features
- `--sort`    — Sort by `alpha`, `artist`, or `date`
- `--random`  — Shuffle output tracks
- `--nodup`   — Prevent adding duplicates
- `--force`   — Allow operations where source and dest are the same

## License

This project is licensed under the [MIT License](LICENSE).