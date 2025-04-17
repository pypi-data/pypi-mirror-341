import json
import os
import time

import spotipy
from InquirerPy import inquirer
from InquirerPy.separator import Separator
from spotipy.oauth2 import SpotifyOAuth


class SpotifyClient:
    def __init__(self, config_file, scope):
        self.config_file = config_file
        self.scope = scope
        self.cache_path = os.path.expanduser("~/.spotifyclient/.cache")
        self.sp = self.get_spotify_client()

    def setup(self):
        """Setup Spotify client credentials."""
        print("Setup command is running...")
        try:
            config = self.load_config() or {}

            client_id = input(
                f"Enter Client ID [{config.get('client_id', '')}]: "
            ) or config.get("client_id")
            client_secret = input(
                f"Enter Client Secret [{config.get('client_secret', '')}]: "
            ) or config.get("client_secret")
            redirect_uri = input(
                f"Enter Redirect URI [{config.get('redirect_uri', 'http://127.0.0.1:8888/callback')}]: "
            ) or config.get("redirect_uri", "http://127.0.0.1:8888/callback")

            config.update(
                {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                }
            )

            self.save_config(config)
            print("Configuration saved successfully.")
        except Exception as e:
            print(f"Error during setup: {e}")

    def load_config(self):
        try:
            if not os.path.exists(self.config_file):
                return None
            with open(self.config_file, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading config: {e}")
            return None

    def save_config(self, config):
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, "w") as file:
                json.dump(config, file)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_spotify_client(self):
        try:
            config = self.load_config()
            if not config:
                self.setup()
                config = self.load_config()

            return spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=config["client_id"],
                    client_secret=config["client_secret"],
                    redirect_uri=config["redirect_uri"],
                    scope=self.scope,
                    cache_path=self.cache_path,
                )
            )
        except Exception as e:
            print(f"Error getting Spotify client: {e}")
            return None

    def _get_cache_path(self, filename):
        return os.path.join(os.path.expanduser("~/.spotifyclient"), filename)

    def _load_cache(self, filename):
        try:
            path = self._get_cache_path(filename)
            if not os.path.exists(path):
                return None
            with open(path, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error reading cache {filename}: {e}")
            return None

    def _save_cache(self, filename, data):
        try:
            os.makedirs(os.path.dirname(self._get_cache_path(filename)), exist_ok=True)
            with open(self._get_cache_path(filename), "w") as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Error writing cache {filename}: {e}")

    def get_all_playlists(self):
        try:
            cache = self._load_cache("playlists_cache.json")
            current_time = time.time()

            if cache and current_time - cache["timestamp"] < 120:
                return cache["data"]

            playlists = []
            results = self.sp.current_user_playlists()
            playlists.extend(results["items"])

            while results["next"]:
                results = self.sp.next(results)
                playlists.extend(results["items"])

            self._save_cache(
                "playlists_cache.json", {"timestamp": current_time, "data": playlists}
            )

            return playlists
        except Exception as e:
            print(f"Error getting playlists: {e}")
            return []

    def get_playlist_tracks(self, playlist_id):
        try:
            filename = f"tracks_cache_{playlist_id}.json"
            cache = self._load_cache(filename)
            current_time = time.time()

            if cache and current_time - cache["timestamp"] < 120:
                return cache["data"]

            tracks = []
            results = self.sp.playlist_tracks(playlist_id)
            tracks.extend(results["items"])

            while results["next"]:
                results = self.sp.next(results)
                tracks.extend(results["items"])

            self._save_cache(filename, {"timestamp": current_time, "data": tracks})

            return tracks
        except Exception as e:
            print(f"Error getting playlist tracks: {e}")
            return []

    def search_song(self, query):
        """Search for a song by name."""
        try:
            results = self.sp.search(q=query, type="track", limit=10)
            tracks = results["tracks"]["items"]
            return tracks
        except Exception as e:
            print(f"Error searching for song: {e}")
            return []

    def list_playlists(self):
        playlists = self.get_all_playlists()
        playlist_choices = [
            {"name": f"{idx + 1}: {playlist['name']}", "value": playlist}
            for idx, playlist in enumerate(playlists)
        ]

        selected_playlist = inquirer.select(
            message="Select a playlist:",
            choices=playlist_choices,
        ).execute()

        return selected_playlist

    def list_songs(self, playlist):
        try:
            tracks = self.get_playlist_tracks(playlist["id"])
            track_choices = [
                {
                    "name": f"{idx + 1}. {track['track']['name']} by {', '.join(artist['name'] for artist in track['track']['artists'])}",
                    "value": track,
                }
                for idx, track in enumerate(tracks)
            ]

            def search_songs():
                search_query = inquirer.text(
                    message="Enter a search term to filter songs:"
                ).execute()
                if search_query:
                    filtered_choices = [
                        choice
                        for choice in track_choices
                        if search_query.lower() in choice["name"].lower()
                        or any(
                            search_query.lower() in artist["name"].lower()
                            for artist in choice["value"]["track"]["artists"]
                        )
                    ]
                    return inquirer.select(
                        message="Select a song to play:",
                        choices=[
                            {"name": "Play entire playlist", "value": "play_all"},
                            Separator(),
                        ]
                        + filtered_choices,
                        cycle=True,
                    ).execute()
                return None

            selected_track = inquirer.select(
                message="Select a song to play:",
                choices=[
                    {"name": "Play entire playlist", "value": "play_all"},
                    {"name": "Search in playlist", "value": "search"},
                    Separator(),
                ]
                + track_choices,
                cycle=True,
            ).execute()

            if selected_track == "search":
                selected_track = search_songs()

            return selected_track
        except Exception as e:
            print(f"Error listing songs: {e}")
            return None

    def list_devices(self):
        try:
            devices = self.sp.devices()["devices"]
            if not devices:
                print(
                    "No devices found. Please open Spotify on a device to activate it."
                )
                return None

            if len(devices) == 1:
                print("Only one device found, hence skipping choice")
                return devices[0]["id"]

            device_choices = [
                {
                    "name": f"{device['name']} ({'Active' if device['is_active'] else 'Inactive'})",
                    "value": device["id"],
                }
                for device in devices
            ]

            selected_device_id = inquirer.select(
                message="Select a device to play on:",
                choices=device_choices,
            ).execute()

            return selected_device_id
        except Exception as e:
            print(f"Error listing devices: {e}")
            return None
