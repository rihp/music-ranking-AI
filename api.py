import os
import pandas as pd
from datetime import date
from flask import Flask, request, app

# My modules:
from src.config import PORT
from src.controllers import mongo_handler as mah
from src.controllers import chartmetric_handler as cmh
from src.controllers import spotify_handler as sfh
from src.predictor import predict, predictions_to_json

# FLASK SETUP
app = Flask(__name__)

@app.route("/")
def landing_page():
    #return home_html
    return {'message':
    f'Hello, world! Welcome to my Music Prediction API.'}
    
@app.route("/api/artist/<spotify_artist_id>/predict")
def predict_artist(spotify_artist_id, n_periods=30, since="2020-01-01", until=date.today().isoformat()):
    """
    Input:  A dataframe with a datetime index and the number of periods to predict
    Output: The `_id` of the created document in Mongo Atlas
    """
    platform = 'spotify'       # The base artist ids we use to identify all artists

# 1. Query Available data for the specified `artist_id` in all external data sources. 
    query_params = { "since":since, "until":until }
    
    # Prepare present data about the artist
    sf_data = sfh.q_spotify(spotify_artist_id)

    # Prepare historic data about the artist
    cm_data = cmh.q_chartmetric(platform, spotify_artist_id, **query_params)
    df = cm_data.copy()    

    #df = pd.concatenate((chartmetric_data,spotify_data, trends_data), axis=1)


# 2. Generate prediction with ARIMA
    pred_df = predict(df, n_periods=n_periods)

# 3. Send time-series prediction to Mongo Atlas
    preds_json = list(predictions_to_json(pred_df, until))

    message = mah.send_to_database(sf_data, preds_json)
    return message

@app.route("/api/<artist_id>/lookup")
def artist_lookup(artist_id):
    """
    Query in MongoAtlas the predictions for the specified artist_id
    Look for recent news and other relevant (PRESENT) data. 
    Return data as a JSON
    """
    return {"message":"app under development"}

@app.route("/api/<artist_id>/report")
def artist_report(artist_id):
    """
    Uses the `artist_lookup` endpoint  to leverage on the JSON response
    Draws a group of matplotlib graphs
    Displays available data as a basic HTML UI
    Sends a tweet with the generated report
    """
    return {"message":"app under development"}

app.run(host="0.0.0.0", port=PORT, debug=True)