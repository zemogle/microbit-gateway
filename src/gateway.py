import microbit
import time
from datetime import datetime, timedelta
import spotipy
import spotipy.util as util
from spotipy.client import SpotifyException
import random

from config import *

def spotify_init():
    return util.prompt_for_user_token(username=USERNAME,
            scope=SCOPES,
            client_id=CLIENTID,
            client_secret=CLIENTSECRET,
            show_dialog=False,
            redirect_uri='http://www.gomez.me.uk/')

def spotify_randomiser(token):
    sp = spotipy.Spotify(auth=token)
    pl = sp.user_playlist(user=USERNAME,playlist_id='spotify:playlist:{}'.format(PLAYLISTID))
    tracknum = random.randint(0,pl['tracks']['total'])-1
    track = pl['tracks']['items'][tracknum]['track']['uri']
    artists = [a['name'] for a in pl['tracks']['items'][tracknum]['track']['artists']]
    print('{} by {}'.format(pl['tracks']['items'][tracknum]['track']['name'], ", ".join(artists)))
    sp.start_playback(device_id=DEVICE, uris=[track])
    return True


if __name__ == '__main__':
    print("gateway running")
    lasttime = datetime.now() - timedelta(minutes=10)
    sent = False
    lastmsg = False
    token = TOKEN
    while True:
        msg = microbit.get_next_message()
        if msg:
            sent = False
            lastmsg = msg
            lasttime = datetime.now()
        timesep = (datetime.now() - lasttime).total_seconds()
        if not msg and timesep > 0.1 and timesep < 2 and not sent :
            # Was there a message and has it been quiet since
            # Wait 0.1s so we don't get multiple hits from the one button push
            try:
                sent = spotify_randomiser(token)
            except SpotifyException as e:
                print('Trying again to get token {}'.format(e))
                token = spotify_init()
                sent = spotify_randomiser(token)
