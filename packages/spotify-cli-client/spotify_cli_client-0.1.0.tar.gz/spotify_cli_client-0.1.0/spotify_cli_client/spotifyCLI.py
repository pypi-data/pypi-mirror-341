from InquirerPy import inquirer

from .spotifyClient import SpotifyClient


class SpotifyCLI:
    def __init__(self, config_file, scope):
        self.client = SpotifyClient(config_file, scope)

    def init(self):
        """List all available features and execute the selected one."""
        choices = [
            {"name": "My Playlists", "value": self.my_playlists},
            {"name": "Search a Song", "value": self.search},
        ]

        selected_action = inquirer.select(
            message="Select a feature to use:",
            choices=choices,
        ).execute()

        # Execute the selected action
        selected_action()

    def my_playlists(self):
        """Play songs from your playlists."""
        try:
            device_id = self.client.list_devices()
            if not device_id:
                print(
                    "No active device selected. Please activate a device and try again."
                )
                return

            selected_playlist = self.client.list_playlists()
            while True:
                selected_track = self.client.list_songs(selected_playlist)

                if selected_track == "play_all":
                    self.client.sp.start_playback(
                        device_id=device_id, context_uri=selected_playlist["uri"]
                    )
                    print(f"Playing entire playlist: {selected_playlist['name']}")
                    break
                else:
                    # Check if a song is currently playing
                    current_playback = self.client.sp.current_playback()
                    if current_playback and current_playback["is_playing"]:
                        print("Keybindings: a -> Add to queue, p -> Play current song")
                        keybinding = input("Enter your choice: ").strip().lower()

                        if keybinding == "a":
                            self.client.sp.add_to_queue(
                                selected_track["track"]["uri"], device_id=device_id
                            )
                            print(
                                f"Added to queue: {selected_track['track']['name']} by {', '.join(artist['name'] for artist in selected_track['track']['artists'])}"
                            )
                        elif keybinding == "p":
                            self.client.sp.start_playback(
                                device_id=device_id,
                                uris=[selected_track["track"]["uri"]],
                            )
                            print(
                                f"Playing song: {selected_track['track']['name']} by {', '.join(artist['name'] for artist in selected_track['track']['artists'])}"
                            )
                        else:
                            print("Invalid keybinding.")
                            break
                    else:
                        self.client.sp.start_playback(
                            device_id=device_id, uris=[selected_track["track"]["uri"]]
                        )
                        print(
                            f"Playing song: {selected_track['track']['name']} by {', '.join(artist['name'] for artist in selected_track['track']['artists'])}"
                        )
                        break
        except Exception as e:
            print(f"Error during my_playlists: {e}")

    def search(self):
        """Search for a song and display results."""
        try:
            while True:
                query = input("Enter song name to search (or 'exit' to leave): ")
                if query.lower() == "exit":
                    break

                tracks = self.client.search_song(query)
                if not tracks:
                    print("No songs found.")
                    continue

                track_choices = [
                    {
                        "name": f"{idx + 1}. {track['name']} by {track['artists'][0]['name']}",
                        "value": track,
                    }
                    for idx, track in enumerate(tracks)
                ]

                selected_track = inquirer.select(
                    message="Select a song to play:",
                    choices=track_choices,
                ).execute()

                device_id = self.client.list_devices()
                if not device_id:
                    print(
                        "No active device selected. Please activate a device and try again."
                    )
                    return

                # Check if a song is currently playing
                current_playback = self.client.sp.current_playback()
                if current_playback and current_playback["is_playing"]:
                    print("Keybindings: a -> Add to queue, p -> Play current song")
                    keybinding = input("Enter your choice: ").strip().lower()

                    if keybinding == "a":
                        self.client.sp.add_to_queue(
                            selected_track["uri"], device_id=device_id
                        )
                        print(
                            f"Added to queue: {selected_track['name']} by {selected_track['artists'][0]['name']}"
                        )
                    elif keybinding == "p":
                        self.client.sp.start_playback(
                            device_id=device_id, uris=[selected_track["uri"]]
                        )
                        print(
                            f"Playing song: {selected_track['name']} by {selected_track['artists'][0]['name']}"
                        )
                    else:
                        print("Invalid keybinding.")
                else:
                    self.client.sp.start_playback(
                        device_id=device_id, uris=[selected_track["uri"]]
                    )
                    print(
                        f"Playing song: {selected_track['name']} by {selected_track['artists'][0]['name']}"
                    )
        except Exception as e:
            print(f"Error during search: {e}")

    def play(self):
        try:
            self.client.sp.start_playback()
            print("Resuming playback.")
        except Exception as e:
            print(f"Error resuming playback: {e}")

    def play_next(self):
        try:
            self.client.sp.next_track()
            print("Playing next track.")
        except Exception as e:
            print(f"Error playing next track: {e}")

    def play_prev(self):
        try:
            self.client.sp.previous_track()
            print("Playing previous track.")
        except Exception as e:
            print(f"Error playing previous track: {e}")

    def pause(self):
        try:
            self.client.sp.pause_playback()
            print("Playback paused.")
        except Exception as e:
            print(f"Error pausing playback: {e}")

    def stop(self):
        # device_id = self.client.list_devices()
        try:
            self.client.sp.pause_playback()
            self.client.sp.seek_track(position_ms=0)
            print("Music stopped.")
        except Exception as e:
            print(f"Error stopping music: {e}")
