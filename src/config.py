# -------------------------------------------------------- #
#                           dotenv                         #
# -------------------------------------------------------- #
from dotenv import load_dotenv
load_dotenv()

# -------------------------------------------------------- #
#                         Database                         #
# -------------------------------------------------------- #
from src.controllers import mongo_handler

# -------------------------------------------------------- #
#                          Flask                           #
# -------------------------------------------------------- #
flask_api = 'http://localhost:5007'    
github_profile="https://github.com/rihp"
repo_url="https://github.com/rihp/music-ranking-ai"
PORT=5007

# -------------------------------------------------------- #
#                   External Data Sources                  #
# -------------------------------------------------------- #
from src.controllers import chartmetric_handler, spotify_handler

# -------------------------------------------------------- #
#                   Documents and paths                    #
# -------------------------------------------------------- #
google_trends_raw_data_path = f"OUTPUT/data/google_trends_raw"
google_trends_dataset_path = f"OUTPUT/data/google_trends_dataset"
OUTPUT_models_trained_path = 'OUTPUT/trained_models/'

# -------------------------------------------------------- #
#           Global variables (necessary for cronjobs)      #
# -------------------------------------------------------- #
playlist_id = "2CKZeXLUX4Z73DT7AThlfb"
playlist_uid = "spotify:playlist:2CKZeXLUX4Z73DT7AThlfb"
