#/usr/bin/pythoi!env python
# -*- coding: UTF-8

import sys
import spotipy
import spotipy.util as util

scope = 'playlist-modify-public'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)


def get_artist_by_name(name):
    artist_results = sp.search(q='artist:' + artist, type='artist')
    artist_items = artist_results['artists']['items']
    if len(artist_items) > 0:
        return artist_items[0]['id']

def get_playlists():
    names = {}
    for list in sp.current_user_playlists()['items']:
        names[list['name']] = list['id']
    return names

def get_counter(artist_name):
    try:
        file = open('{}.txt'.format(artist_name), 'r+')
        counter = int(file.read())
        file.seek(0)
        file.write(str(counter + 1))
        return counter
    except IOError:
        file = open('{}.txt'.format(artist_name), 'w')
        file.write(str(0))
        return 0

def reset_counter(artist_name):
    file = open('{}.txt'.format(artist__name), 'r+')
    file.seek(0)
    file.write(str(0))


if token:
    sp = spotipy.Spotify(auth=token)
    artists = ['Die drei ???', 'Benjamin Blümchen']
    blacklist = ['und der schwarze Tag (Sechs Kurzgeschichten)']

    for artist in artists:

        # Create the pubplic playlist if it does not exist
        artist_id = get_artist_by_name(artist)
        playlist_name = '{} Folge des Tages'.format(artist)
        playlists = get_playlists()
        if not playlist_name in playlists.keys():
            print('Creating playlist {}'.format(playlist_name))
            playlist = sp.user_playlist_create(username,playlist_name, public=True, description='Test PL')
            playlists = get_playlists()
            
        # Get all albums from the artist
        print('Getting albums for {}'.format(artist))
        artist_url = 'spotify:artist:{}'.format(artist_id)
        results = sp.artist_albums(artist_url, album_type='album')
        albums = results['items']
        while results['next']:
            results = sp.next(results)
            albums.extend(results['items'])

        # Get all tracks from album
        album_number = get_counter(artist)
        if albums[album_number]['name'] in blacklist:
            print('Skipping album #{} "{}"'.format(album_number, albums[album_number]['name']))
            album_number = get_counter(artist)
        try:
            print('Getting album #{} with name "{}"'.format(album_number, albums[album_number]['name']))
            album_track_results = sp.album_tracks(albums[album_number]['id'])
        except IndexError:
            print('Reached end of albums ({}), start from beginning'.format(album_number))
            reset_counter(artist)
            album_number=0
            print('Getting album # {} with name {}'.format(album_number, albums[album_number]['name']))
            album_track_results = sp.album_tracks(albums[album_number]['id'])

        album_tracks = album_track_results['items']
        while album_track_results['next']:
            album_track_results = sp.next(album_track_results)
            album_tracks.extend(album_track_results['items'])

        # Add track to playlist

        track_ids = []
        for track in album_tracks:
            track_ids.append(track['id'])
        print('Adding {} tracks to playlist {}'.format(len(track_ids),playlist_name))
        try:
            sp.user_playlist_replace_tracks(username, playlists[playlist_name], track_ids)
        except spotipy.client.SpotifyException:
            sp.user_playlist_replace_tracks(username, playlists[playlist_name], track_ids[:99])
            sp.user_playlist_add_tracks(username, playlists[playlist_name], track_ids[99:])
else:
    print("Can't get token for", username)
