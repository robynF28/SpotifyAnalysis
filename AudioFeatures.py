# shows acoustic features for tracks for the given artist

from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys
import spotipy.util as util


f = open('Features.txt','w')

token = util.prompt_for_user_token('victoria2900',
                           'user-top-read',
                           client_id='d7696b97174d43e9b935035d0149beb2',
                           client_secret='fb369e7239314ee09e0cecbf0c352a27',
                           redirect_uri='http://localhost:8888/callback/')
sp = spotipy.Spotify(auth=token)
sp.trace = True

if len(sys.argv) > 1:
    tids = sys.argv[1:]
    print(tids)

    start = time.time()
    features = sp.audio_features(tids)
    delta = time.time() - start
    print(json.dumps(features, indent=4))
   ## f.write(json.dumps(features, indent=4)[0].{10})
    with f as outfile:
        json.dump("{featuresData: ", outfile)
        json.dump(features, outfile)
        json.dump("}", outfile)
    print("features retrieved in %.2f seconds" % (delta,))