import os, datetime, json, requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

####################################
# SPOTIFY                          #
####################################
from src.config import SCID
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def get_artist_id(artist_id):
    pass

def get_artist(artist_id):
    """
    Endpoint : https://api.spotify.com/v1/artists/{id}   
    """
    res = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}")
    return 

def get_spotify_ranking(artist_id, start=None, end=None):
    """
    https://developer.spotify.com/documentation/web-api/

    INPUT:
        - spotify artist_id
        - start and end dates 
    OUTPUT:
        - JSON timeseries of the artist ranking
    """
    # Set API Query parameters
    params = dict(
        client_id=os.getenv('SCID'),
        client_secret=os.getenv('SCS'),
        limit=limit
    )

    print(f"Requesting: {url} \n - Time Window = {start}:{end}" )

    # Make HTTP request
    response = requests.get(url=url, params=params)
    print(response.status_code) #https://http.cat/

    return response
