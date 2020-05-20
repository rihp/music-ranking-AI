import os, json, requests
from src import utils
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
cm_api_url = "https://api.chartmetric.com/api/"

# -------------------------------------------------------- #
#                 Request access token                     #
# -------------------------------------------------------- #
CMRT= os.getenv("CMRT") # Load refresh token

def req_chartmetric_token():
    """
    Uses the secret refresh token to generate a temporary access token
    Input: None
    Output: HTTP Header configured with the temporary acces token
    """
    authURL = f"{cm_api_url}token"
    headers = {"Content-Type": "application/json"}
    refreshtokenkey = "refreshtoken"
    refreshtoken = CMRT
    data = "{" + f'"{refreshtokenkey}":"{refreshtoken}"' + "}"
    response = requests.post(authURL, headers=headers, data=data)

    if not response.ok:  
        # raise if exception if there is an issue with the request
        response.raise_for_status()

    # Load access token and prepare requests url and headers.
    ACCESS_TOKEN = json.loads(response.text)['token']
    cm_headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    print("A new token access token for chartmetric has been generated. It should expire in one hour.")
    return cm_headers

# -------------------------------------------------------- #
#                     Requesting  Data                     #
# -------------------------------------------------------- #
def get_cm_artist_id(platform, platform_id):
    """
    @ Endpoint = https://api.chartmetric.com/api/artist/:type/:id/get-ids
    INPUT: platform and artist_id as strings
    OUTPUT: Chartmetric artist ID as a type `int`
    """
    print(f"{utils.isotime()} - Requesting Artist ID")

    # Configure Endpoint
    cm_headers = req_chartmetric_token()
    endpoint = f"{cm_api_url}artist/{platform}/{platform_id}/get-ids"
    
    # Make Request
    response = requests.get(endpoint, headers=cm_headers)
    print(f"{utils.isotime()} - {response}")
    
    
    if platform == 'spotify':
        cm_artist_id = json.loads(response.text)['obj'][0]['cm_artist']
    else:
        raise Exception('This platform has not yet been configured internally. Try using a `spotify_id`')
    return cm_artist_id

def get_cpp_data(cm_artist_id, stat='rank', since=None, until=None):
    """
    INPUT: query parameters
    OUTPUT: JSON with CPP datapoints
    """
    print(f"{utils.isotime()} - Requesting Artist CPP data. ({stat=}, {since=}, {until=})")
    if stat not in ("rank", "score"): raise Exception('Specified unvalid CPP stat.')
    if (type(since) != str) or (type(until) != str): raise Exception("Use iso format 'YYYY-MM-DD'")
    
    # Configure Endpoint
    cm_headers = req_chartmetric_token()
    endpoint = f"{cm_api_url}artist/{cm_artist_id}/cpp?stat={stat}&since={since}&until={until}"

    # Make Request
    response = requests.get(endpoint, headers=cm_headers)
    print(f"{utils.isotime()} - {response}")

    return response.json()['obj']

def get_daily_listeners(artist_id, start=None, end=None):
    """
    Looks up an artist in the chartmetric database.
    Converts the JSON response of all the historic values into a dataframe with a datetime index
    """
    return df

def get_spotify_ranking_history(artist_id, start=None, end=None):
    """
    https://developer.spotify.com/documentation/web-api/

    INPUT:
        - spotify artist_id
        - start and end dates 
    OUTPUT:
        - JSON timeseries of the artist ranking
    """
    # Set API Query parameters
    """
    params = dict(
        client_id=client_id,
        client_secret=os.getenv('SCS'),
        limit=limit
    )

    print(f"Requesting: {url} \n - Time Window = {start}:{end}" )

    # Make HTTP request
    response = requests.get(url=url, params=params)
    print(response.status_code) #https://http.cat/
    return response
    """
    pass

# -------------------------------------------------------- #
#                 Query All Necessary Data                 #
# -------------------------------------------------------- #
def q_chartmetric(platform, platform_id, since=None, until=None):
    """
    INPUT: query params
    OUTPUT: dataframe with datetime index
    """
    cm_artist_id = get_cm_artist_id(platform, platform_id)
    historic_data_arr = get_cpp_data(cm_artist_id, stat='rank', since=since, until=until)
    df = jsons_to_datetime_df(historic_data_arr)
    return df

# -------------------------------------------------------- #
#                  Transforming Responses                  #
# -------------------------------------------------------- #
def jsons_to_datetime_df(historic_data_arr):
    """
    INPUT: array of shape:
                [{'rank': 4, 'timestp': '2020-05-14T00:00:00.000Z'},
                    (...),
                {'rank': 5, 'timestp': '2020-05-13T00:00:00.000Z'},]
    
    OUTPUT: dataframe with datetime index
    """
    rank_history = {}
    for e in historic_data_arr:
        rank_history.update({e['timestp']:e['rank']})
    df = pd.DataFrame(rank_history.values(), index=rank_history.keys())
    df.index = pd.to_datetime(df.index)
    return df