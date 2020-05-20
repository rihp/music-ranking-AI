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
def no_spaces(string):
    return string.replace(' ', '_')

def send_to_database(artist_id, predictions_json):
    """
    Updates MongoAtlas with the new prediction
    """
    # Prepare the doc to be sent
    doc  = {# ♠ Optimization: Use BSON ObjectId - https://api.mongodb.com/python/current/api/bson/objectid.html                
            '_id':artist_id,
            'name':"ARTIST NAME HERE",
            'generated': utils.isotime(brackets=False),
            'predictions': predictions_json
        }

    try:
        db.predictions.insert_one( doc ).inserted_id
    except DuplicateKeyError:
        db.predictions.replace_one(
                            # Replace this document
                            { "_id" : artist_id },    
                            # With this new document
                            doc )
    return {"message": f"sent item to atlas with _id:{artist_id}"}