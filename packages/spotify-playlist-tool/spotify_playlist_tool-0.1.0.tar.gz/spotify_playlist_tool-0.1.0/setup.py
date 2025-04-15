from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="spotify_playlist_tool",
    version="0.1.0",
    description="A CLI tool for managing Spotify playlists.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Gretchen Maculo",
    license="MIT",
    packages=find_packages(),
    install_requires=["spotipy"],
    entry_points={
        "console_scripts": [
            "spotify_playlist_tool=spotify_playlist_tool.tool:main",
            "spotify-tool=spotify_playlist_tool.tool:main"
        ],
    },
    python_requires=">=3.7",
)

