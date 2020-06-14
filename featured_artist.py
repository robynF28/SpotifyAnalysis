import time
import numpy as np

import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
#https://medium.com/@RareLoot/extracting-spotify-data-on-your-favourite-artist-via-python-d58bc92a4330
cid = '7db022f9b43943f99dee6b518c99cf35'
csecret = 'e95b70817aec4486b9dc0226e72b5c79'

cmanager = SpotifyClientCredentials (
    client_id=cid,
    client_secret=csecret
)

sp = spotipy.Spotify(client_credentials_manager=cmanager)

name = "Ed Sheeran"

result = sp.search(name)
print(result['tracks']['items'][0]['artists'])
print()
artist_uri = result['tracks']['items'][0]['artists'][0]['uri']

sp_albums = sp.artist_albums(artist_uri, album_type='album')

# store artist's albums' names' and uris in separate lists
album_names = []
album_uris = []
for i in range(len(sp_albums['items'])):
    album_names.append(sp_albums['items'][i]['name'])
    album_uris.append(sp_albums['items'][i]['uri'])

print(album_names)
print(album_uris)
print('\n')

spotify_albums = {}
album_count = 0

# extracting songs from each album
def albumSongs(uri):
    album = uri
    # dictionary for that specific album
    spotify_albums[album] = {}

    # creating key values of empty lists inside nested dictionary
    spotify_albums[album]['album'] = []
    spotify_albums[album]['track_number'] = []
    spotify_albums[album]['id'] = []
    spotify_albums[album]['name'] = []
    spotify_albums[album]['uri'] = []

    tracks = sp.album_tracks(album) # pulling data from album tracks

    for n in range(len(tracks['items'])):
        # parses through each song;s track
        spotify_albums[album]['album'].append(album_names[album_count])
        spotify_albums[album]['track_number'].append(tracks['items'][n]['track_number'])
        spotify_albums[album]['id'].append(tracks['items'][n]['id'])
        spotify_albums[album]['name'].append(tracks['items'][n]['name'])
        spotify_albums[album]['uri'].append(tracks['items'][n]['uri'])

for i in album_uris:
    albumSongs(i)
    print("Album " + str(album_names[album_count]) + 
    " songs added to spotify_albums dictionary")
    album_count += 1

# stopped at audio_features
def audio_features(album):
    # adds new key-values to store audio features
    spotify_albums[album]['acousticness'] = []
    spotify_albums[album]['danceability'] = []
    spotify_albums[album]['energy'] = []
    spotify_albums[album]['instrumentalness'] = []
    spotify_albums[album]['liveness'] = []
    spotify_albums[album]['loudness'] = []
    spotify_albums[album]['speechiness'] = []
    spotify_albums[album]['tempo'] = []
    spotify_albums[album]['valence'] = []
    spotify_albums[album]['popularity'] = []

    # creates track counter
    track_count = 0
    for track in spotify_albums[album]['uri']:
        # pull audio features per track
        features = sp.audio_features(track)

        # append to relevant key-value
        spotify_albums[album]['acousticness'].append(features[0]['acousticness'])
        spotify_albums[album]['danceability'].append(features[0]['danceability'])
        spotify_albums[album]['energy'].append(features[0]['energy'])   
        spotify_albums[album]['instrumentalness'].append(features[0]['instrumentalness'])
        spotify_albums[album]['liveness'].append(features[0]['liveness'])
        spotify_albums[album]['loudness'].append(features[0]['loudness'])
        spotify_albums[album]['speechiness'].append(features[0]['speechiness'])
        spotify_albums[album]['tempo'].append(features[0]['tempo'])
        spotify_albums[album]['valence'].append(features[0]['valence'])

       #popularity is stored elsewhere
        pop = sp.track(track)
        spotify_albums[album]['popularity'].append(pop['popularity'])
        track_count+=1

print('\n')

# loop through the albums to extract audio features
sleep_min = 2
sleep_max = 5
start_time = time.time()
request_count = 0

for i in spotify_albums:
    audio_features(i)
    request_count += 1
    if request_count % 5 == 0:
        print(str(request_count) + " playlists completed")
        time.sleep(np.random.uniform(sleep_min, sleep_max))
        print(f'Loop #: {request_count}')
        print(f'Elapsed Time: {time.time() - start_time} seconds')

# organizing data into dataframe
dic_df = {}

dic_df['album'] = []
dic_df['track_number'] = []
dic_df['id'] = []
dic_df['name'] = []
dic_df['uri'] = []
dic_df['acousticness'] = []
dic_df['danceability'] = []
dic_df['energy'] = []
dic_df['instrumentalness'] = []
dic_df['liveness'] = []
dic_df['loudness'] = []
dic_df['speechiness'] = []
dic_df['tempo'] = []
dic_df['valence'] = []
dic_df['popularity'] = []

for album in spotify_albums:
    for feature in spotify_albums[album]:
        dic_df[feature].extend(spotify_albums[album][feature])

print(len(dic_df['album']))

# converting to dataframe
df = pd.DataFrame.from_dict(dic_df)
print(df)

# removing duplicates
print(len(df))
final_df = df.sort_values('popularity',
    ascending = False).drop_duplicates('name').sort_index()
print(len(final_df))




