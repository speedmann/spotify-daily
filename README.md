# spotify-daily
Creates playlists for audiobooks which can be updated daily

This script fetches all available albums from specified artists and creates a playlist for one of these albums.
On every subsequent run, it will increase a counter an will choose the next available album.
If no albums are available anymore, it will start over.

# Installation
```
pip install -r requirements.txt
```

# Usage
## Spotify setup
Go to https://developer.spotify.com/ and create a new application.
Enter a valid url for the redirection.

export these variables
```
SPOTIPY_CLIENT_ID=<your client id>
SPOTIPY_CLIENT_SECRET=<your client secret>
SPOTIPY_REDIRECT_URI=<your redirect url>
```

# Modify `create_playlist.py`
To include your wanted artists, change
```
    artists = ['Die drei ???', 'Benjamin Blümchen']
```
to whatever artists you want.
# execute
```
 python create_playlist.py <username>
```

This will open a webbrowser which requests a login to your spotify account. Login to your account and copy the URL to the terminal.


# Todo

When a new album is added, this script will not recognize it, it will go on with it's stupid simple counter and will update the playlist with the same album again...
