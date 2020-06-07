import sys
import spotipy
import spotipy.util as util
import lyricsgenius as genius

token = util.prompt_for_user_token(username='robynfajardo01',
                            scope='user-read-currently-playing',
                            client_id= '6c3110a33f834e5ca8d856d56b634e57',
                            client_secret= '21e6b3efa75a4cdcb73f77ec1f198803',
                            redirect_uri= 'http://localhost:8888/callback/')


# def show_lyrics(tracks):
#get access to Genius.com's lyrics
api = genius.Genius("E66l13QmPc8mC_0IPfZWhy7oaah7pztJ705Cj-_QWP1pOxwDMDdnKjDWxHh0shaZ")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python user_playlists.py [username]")
        sys.exit()

# shows song name and artist
if token:
    sp = spotipy.Spotify(auth=token)
    current_song = sp.currently_playing()
    artist_name = current_song['item']['artists'][0]['name']
    name_song = current_song['item']['name']
    print(artist_name, name_song)
else:
    print("Can't get token for", username)


# show lyrics
if token:
    sp = spotipy.Spotify(auth=token)
    current_song = sp.currently_playing()
    artist = current_song['item']['artists'][0]['name']
    name_song = current_song['item']['name']
    song = api.search_song(name_song, artist)
    print(song.lyrics)
else:
    print("Can't get token for", username)