#! /home/guido/miniconda3/envs/spotify/bin/python

import yaml
import time
import json
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from datetime import datetime, date, timedelta

with open("config.yml", "r") as yml_file:
    cfg = yaml.safe_load(yml_file)

spotify = cfg["spotify_api"]
auth = SpotifyOAuth(
    client_id = spotify["client_id"],
    client_secret=spotify["client_secret"],
    redirect_uri=spotify["redirect_uri"],
    scope=spotify["scope"],
    open_browser=False)
sp = spotipy.Spotify(auth_manager=auth)
    
def to_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%X.%fZ")

def get_artist_names(artists_list):
    names = [artist["name"] for artist in artists_list]
    return ", ".join(names)

def get_played_songs():
    today = datetime(
            date.today().year,
            date.today().month,
            date.today().day
            )
    yesterday = today - timedelta(days=1)
    
    full_songs = []
    for h in range(0, 24, 2):
        after_date = yesterday + timedelta(hours=h) - timedelta(hours=3)
        after_date = int(datetime.timestamp(after_date))
        data = sp.current_user_recently_played(limit=50, after=after_date)

        songs = map(
            lambda x: {
                "played_at": x["played_at"],
                "id": x["track"]["id"],
                "name": x["track"]["name"],
                "artists": get_artist_names(x["track"]["artists"])
            },
            data["items"]
        )

        songs = filter(lambda x: x not in full_songs, songs)
        songs = filter(
            lambda x: to_datetime(x["played_at"]).day == yesterday.day,
            songs
        )
        full_songs.extend(songs)

    return full_songs


def get_song_features(songs):
    songs_extended = map(
        lambda track: dict(track, **sp.audio_features(track["id"])[0]),
        songs
    )   

    return songs_extended

def pipeline_plays():
    all_tracks = get_played_songs()
    full_tracks = get_song_features(all_tracks)
    for track in full_tracks:
        print(json.dumps(track))

pipeline_plays()
