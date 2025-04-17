# 🎧 Spotify CLI Client

A powerful and interactive command-line interface to control your Spotify playback using Python and [Spotipy](https://spotipy.readthedocs.io/) with a beautiful TUI powered by [InquirerPy](https://github.com/kazhala/InquirerPy).

---

## 🚀 Features

- 🔍 **Search** for any track and play it instantly.
- 📚 View and play songs from your **personal playlists**.
- ⏯️ Full playback controls: `play`, `pause`, `next`, `prev`, `stop`.
- 🎛️ Intelligent **device selection**.
- ➕ Add tracks to **queue** while music is playing.
- 🔄 Option to **play full playlist** or individual tracks.
- 💾 Stores credentials in a local config file (`~/.spotifyclient/config.json`).

---

## 🛠️ Installation

```bash
pip3 install spotify-cli-client
```

---

## 🎹 Setup

Before using the CLI, set up your Spotify API credentials:

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create an app and get your `Client ID`, `Client Secret`, and `Redirect URI`.

Then run:

```bash
spt init
```

The CLI will prompt you to enter and save your credentials.

---

## 🧠 Usage

```bash
spt <command>
```

### Available Commands

| Command        | Description                         |
| -------------- | ----------------------------------- |
| `init`         | Interactive menu to access features |
| `my_playlists` | Browse and play from your playlists |
| `search`       | Search for a song and play it       |
| `play`         | Resume current playback             |
| `pause`        | Pause the current song              |
| `next`         | Skip to the next track              |
| `prev`         | Play the previous track             |
| `stop`         | Pause and reset playback            |

---

## 📁 Project Structure

```
spotify_cli_client/
├── __init__.py
├── cli.py              # CLI entry using Click
├── spotifyCLI.py       # Interactive CLI wrapper
└── spotifyClient.py    # Spotify API client logic
```

---

## 💡 Example

```bash
$ spt init

? Select a feature to use:
  ▸ My Playlists
    Search a Song
```

---

## 🤝 Contributing

PRs are welcome! Feel free to fork this repo and submit improvements, bugfixes, or new features.

---

## 📜 License

MIT License © 2025 [Sudharshan V](./LICENSE)

---

## 🔗 Credits

- [Spotipy](https://github.com/plamere/spotipy)
- [InquirerPy](https://github.com/kazhala/InquirerPy)
- [Click](https://click.palletsprojects.com/)
