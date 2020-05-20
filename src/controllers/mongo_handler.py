import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.helpers import DuplicateKeyError
from src import utils
load_dotenv()

# -------------------------------------------------------- #
#                       Connection                         #
# -------------------------------------------------------- #
MA = os.getenv("MA")
MAU = os.getenv("MAU")
MSERVER= os.getenv("MSERVER")
PORT= os.getenv("PORT")
DBURL = f"mongodb+srv://{MAU}:{MA}@{MSERVER}/test?retryWrites=true&w=majority"
client = MongoClient(DBURL)
db = client.music
print(f"Connected to MongoClient...  ")

# -------------------------------------------------------- #
#                    Handler functions                     #
# -------------------------------------------------------- #
def send_to_database(sf_data, predictions_json, metric=None):
    """
    Updates MongoAtlas with the new prediction
    """
    # Prepare the doc to be sent
    doc  = {# ♠ Optimization: Use BSON ObjectId - https://api.mongodb.com/python/current/api/bson/objectid.html                
            '_id':sf_data['id'],
            'name':sf_data['name'],
            'last_update': utils.isotime(brackets=False),
            'followers':sf_data['followers'],
            'genres':sf_data['genres'],
            'images':sf_data['images'],
            'popularity':sf_data['popularity'],
            'predictions': predictions_json
        }

    if metric == 'spotify_monthly_listeners': coll = db.spotify_monthly_listeners
    elif metric == 'cpp': coll = db.cpp

    try:
        coll.insert_one( doc ).inserted_id
    except DuplicateKeyError:
        coll.replace_one(
                    # Replace this document
                    { "_id" : sf_data['id'] },    
                    # With this new document
                    doc )
    
    return {"message": f"sent {metric.upper()} to Mongo Atlas with _id:{sf_data['id']}"}