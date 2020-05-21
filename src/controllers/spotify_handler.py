import os, requests
import pandas as pd
import numpy as np
import spotipy
import datetime
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
load_dotenv()

# This should go somewhere else
sample_artist = {"artist_id":'4q3ewBCX7sLwd24euuV69X',
                 "artist_uri":'spotify:artist:4q3ewBCX7sLwd24euuV69X'}

# -------------------------------------------------------- #
#                    Auth / Credentials                    #
# -------------------------------------------------------- #
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
client_id= os.getenv("SPOTIPY_CLIENT_ID")

# -------------------------------------------------------- #
#                    Handler functions                     #
# -------------------------------------------------------- #
def get_artist_id(artist_id):
    pass

def get_artist(artist_id):
    """
    Endpoint : https://api.spotify.com/v1/artists/{id}   
    """
    res = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}")
    return 

def get_artist_albums(artist_uri):
    """
    Output: generator of albums by that artist in JSONs
    """
    results = spotify.artist_albums(artist_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        yield {"name":album['name'],
               "release_date":album['release_date'],
               "total_tracks":album['total_tracks'],
               "uri":album["uri"]
              }


def get_current_popularity(artist_id):
    """
    https://developer.spotify.com/documentation/web-api/

    INPUT:
        - spotify artist_id
    OUTPUT:
        - Current
    """
    # Set API Query parameters
    params = dict(
        client_id=client_id,
        client_secret=os.getenv('SCS'),
        limit=limit
    )

    # Make HTTP request
    response = requests.get(url=url, params=params)
    print(response.status_code) #https://http.cat/
    return response

def scrape_playlist(uri):
#### STEP 01 - GET TRACKS FROM A SPOTIFY PLAYLIST 

    # The query is made here
    playlist = spotify.playlist_tracks(uri)
    playlist.keys()


    # Save all these artists in an array, and then turn it into a set
    my_artists= []
    for song in playlist['items']:
        artists = song['track']['artists']
        for artist in artists:
                my_artists.append((artist['name'], artist['id']))
                
    my_artists = set(my_artists)

#### STEP 02 - GET THE ARTISTS FROM EACH TRACK (ID, NAME, POPULARITY)

    # Use this array to get their current popularity
    my_artists_with_popularity = []
    for e in my_artists:
        my_artists_with_popularity.append([e[0], e[1], spotify.artist(e[1])['popularity']])
    my_artists_with_popularity = pd.DataFrame(my_artists_with_popularity)
    df = my_artists_with_popularity.sort_values(by=2,
                                                    ascending=False).reset_index(drop=True)
    df.columns=['a_name', 'a_id', 'pop']

#### STEP 03 - DEFINE THE TIME INTERVAL TO STUDY (1 WEEK), AND PREPARE PATH FORMATS
    # Prepare the timestamp 
    tmstmp = int(datetime.datetime.today().timestamp())
    output_path = f"OUTPUT/data/google_trends/"

#### STEP 04 - LOAD THE ARTIST'S GOOGLE TREND, OR UPDATE IT:
    scaled = []
    # Try to save each query as a df.to_csv() with a timestamp.
    for i, row in df.iterrows():
        loop_time = f"{datetime.datetime.today().time().hour}:{datetime.datetime.today().minute}"
            
        a_id= row['a_id']
        a_name=row['a_name']
        popularity =row['pop']
        
        try:
            data = pd.read_csv(f"{output_path}trends_{a_id}_{date_start.isoformat()}.csv")
            print(f"data found for {a_name}")
            display(data.head(2))
            scaled.append(data)

        except Exception as e:
            print('it looks like there is no saved data available for that artist...')
            print(f"[{loop_time}] Beginning scrapping process for  Artist: {a_id,a_name}")
            
            # Sleep a second before starting the scrape
            time.sleep(120)
            
            # 1. Query Google trends, returns a dataframe
            data = pytrends.get_historical_interest([a_name], 
                                        year_start=date_start.year, month_start=date_start.month, day_start=date_start.day,
                                        hour_start=0,
                                        year_end  =date_end.year,   month_end=date_end.month,     day_end  =date_end.day,
                                        hour_end  =0,
                                        cat=0, geo='', gprop='', sleep=0)

            # Rename and export
            data.columns = ['trend', 'isPartial']
            data.to_csv(f"{output_path}trends_{a_id}_{date_start.isoformat()}.csv")
            display(data.head(2))
            scaled.append(data)

            # After this loop is done with the last iteration, dont sleep!!
    return scaled

# -------------------------------------------------------- #
#                 Query All Necessary Data                 #
# -------------------------------------------------------- #
def q_spotify(artist_id):
    """
    Output: A doc with relevant data about the artist
    """
    my_artist = spotify.artist(artist_id)
    features = ['id', 'name', 'followers', 'popularity', 'genres', 'images', 'external_urls']
    results = {}
    for key in features:
        results.update({key:my_artist[key]})
    return results

# -------------------------------------------------------- #
#                    Playlists to watch                    #
# -------------------------------------------------------- #
my_playlists = set([
                'spotify:playlist:2CKZeXLUX4Z73DT7AThlfb',
                'spotify:playlist:37i9dQZEVXbLRQDuF5jeBp',
                'spotify:playlist:37i9dQZF1DWTcqUzwhNmKv',
                'spotify:playlist:37i9dQZF1DX5J7FIl4q56G',
                'spotify:playlist:37i9dQZF1DX2LTcinqsO68',
                'spotify:playlist:37i9dQZF1DXcfZ6moR6J0G',
                'spotify:playlist:37i9dQZEVXbLiRSasKsNU9',
                'spotify:playlist:37i9dQZEVXbMDoHDwVN2tF',
                'spotify:playlist:37i9dQZEVXbKuaTI1Z1Afx',
                'spotify:playlist:00AP59Hv6itRPSivUM2enq',
                'spotify:playlist:37i9dQZF1DXe9hay4VT07f',
                'spotify:playlist:37i9dQZF1DXbwoaqxaoAVr',
                'spotify:playlist:37i9dQZF1DWYtKpmml7moA',
                'spotify:playlist:37i9dQZF1DX0KpeLFwA3tO',
                'spotify:playlist:37i9dQZF1DXa9wYJr1oMFq',
                'spotify:playlist:37i9dQZF1DX9wa6XirBPv8',
                'spotify:playlist:37i9dQZF1DX5cO1uP1XC1g',
                'spotify:playlist:37i9dQZF1DXasneILDRM7B',
                'spotify:playlist:37i9dQZF1DX8sGALGjOrTu',
                'spotify:playlist:37i9dQZF1DWWkrGNlIHxPl',
                'spotify:playlist:37i9dQZF1DWYBAUZiPMirH',
                'spotify:playlist:2dQ09eoJnHICGzVNjI1cO8',
                'spotify:playlist:7ylr8m91qYczSGMM41VAka',
                'spotify:playlist:55u6xbZeNSLo1UbTnY1t2T',
                'spotify:playlist:4OaNHYal5khd1vS3yGkqYa',
                'spotify:playlist:5VYgukZjAEYXMX7JLvAx5x',
                'spotify:playlist:6NOKHlcWi0Xjc10iFGd1cB',
                'spotify:playlist:2EBhsE6hqp6p2scwUFXM9t',
                'spotify:playlist:5bGxJbLXuk4Q2yLoC5nIJT',
                'spotify:playlist:4s6G5pQFTG9pMmtnc8f2BQ',
                'spotify:playlist:37i9dQZF1DWTyiBJ6yEqeu',
                'spotify:playlist:37i9dQZF1DWT5MrZnPU1zD',
                'spotify:playlist:37i9dQZF1DX0hvSv9Rf41p',
                'spotify:playlist:37i9dQZF1DXdfOcg1fm0VG',
                'spotify:playlist:37i9dQZF1DX4dyzvuaRJ0n',
                'spotify:playlist:37i9dQZF1DX8tZsk68tuDw',
                'spotify:playlist:37i9dQZF1DWSf2RDTDayIx',
                'spotify:playlist:37i9dQZF1DX0BcQWzuB7ZO',
                'spotify:playlist:37i9dQZF1DWXLeA8Omikj7',
                'spotify:playlist:37i9dQZF1DX6bBjHfdRnza',
                'spotify:playlist:37i9dQZF1DX9tPFwDMOaN1',
                'spotify:playlist:37i9dQZF1DXbirtHQBuwCo',
                'spotify:playlist:37i9dQZF1DX4RDXswvP6Mj',
                ])