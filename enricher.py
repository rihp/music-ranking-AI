import os, datetime, json, requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


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
