#! /home/guido/miniconda3/envs/spotify/bin/python

import yaml

import spotipy
from spotipy.oauth2 import SpotifyOAuth

with open("config.yml", "r") as yml_file:
    cfg = yaml.load(yml_file)

spotify = cfg["spotify_api"]
auth = SpotifyOAuth(
    client_id = spotify["client_id"],
    client_secret=spotify["client_secret"],
    redirect_uri=spotify["redirect_uri"],
    scope=spotify["scope"],
    open_browser=False)
sp = spotipy.Spotify(auth_manager=auth)

try:
    sp.auth_manager.get_access_token(as_dict=True)
    print('token obtenido')
except:
    print('error')