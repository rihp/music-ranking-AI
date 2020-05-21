import os, json
import pandas as pd
import numpy as np
from datetime import date
from flask import Flask, request, app, render_template

# My modules:
from src.utils import hashtag
from src.config import PORT
from src.controllers import mongo_handler as mah
from src.controllers import chartmetric_handler as cmh
from src.controllers import spotify_handler as sfh
from src.predictor import predict, predictions_to_json, clean_df_to_json

# Request data since this date
since="2019-02-01"

# FLASK SETUP
app = Flask(__name__)

@app.route("/")
def landing_page():
    #return home_html
    return {'message':
    f'Hello, world! Welcome to my Music Prediction API.'}

@app.route("/api/artist/<spotify_artist_id>/predict/<metric>")
def predict_artist_metric(spotify_artist_id, metric, n_periods=15, seasonality=7, since=since,
                         until=date.today().isoformat(), platform = 'spotify'):
    """
    Versatile prediction endpoint for a given artist_id and metric.
    Queries data from sources, cleans timeseries, predicts, sends data to MongoAtlas.
    Output: The response of Mongo Atlas Upload.
    """
    # 1. Query Available data for the specified `artist_id` in all external data sources. 
    query_params = { "since":since, "until":until, "metric":metric }   
    sf_data = sfh.q_spotify(spotify_artist_id)                                      # Present data about the artist
    cm_data = cmh.q_chartmetric(platform, spotify_artist_id, **query_params)        # Historic data about the artist
    df = cm_data.copy()    

    # 2. Generate prediction and cleaned data with the defined models
    clean_df, pred_df = predict(df, n_periods=n_periods, seasonality=seasonality, fft=True)
    
    # 3. Send both time-series (hist and pred) to Mongo Atlas
    historic_json = list(clean_df_to_json(clean_df))
    preds_json = list(predictions_to_json(pred_df, until))

    message = mah.send_to_database(sf_data, historic_json, preds_json, metric=metric)
    return message

@app.route("/api/artist/<artist_id>/lookup/<metric>")
def artist_lookup(artist_id, metric):
    """
    Query in MongoAtlas the predictions for the specified artist_id
    Look for recent news and other relevant (PRESENT) data. 
    Return data as a JSON
    """
    doc = mah.lookup_in_database(artist_id, metric=metric)
    return doc

@app.route("/api/artist/<artist_id>/report/<metric>")
def artist_report(artist_id, metric):
    """
    Uses the `artist_lookup` endpoint  to leverage on the JSON response
    Draws a group of matplotlib graphs
    Displays available data as a basic HTML UI
    Sends a tweet with the generated report
    """
    #doc = mah.lookup_in_database(artist_id, metric=metric)
    doc = mah.lookup_in_database(artist_id, metric=metric)

    try:
        a_img = doc['images'][0]['url']
        a_name = doc['name']
        a_genres = ' - '.join([ hashtag(e) for e in doc['genres']])
        a_popularity = doc['popularity']
        a_followers = doc['followers']['total']
        a_href = doc['spotify_href']
        a_updated = doc['last_update'][:10]
        dynamic_vars = {"a_img":a_img, "a_name":a_name, "a_genres": a_genres, "a_popularity":a_popularity,
                        "a_followers":a_followers, "a_href":a_href, "a_updated":a_updated}
        
        check = (doc['past_data'][0], doc['past_data'][0])
        print(type(check), check)

        past_data = doc['past_data']
        pred_data = doc['predictions']
        
        # Invert `y` axis for Cross platform performance
        """        
        if metric == "cpp":
            print(pred_y)
            pred_y = [ e*-1 for e in pred_y]
            print(pred_y)
            past_y = [ e*-1 for e in past_y]"""

        return render_template('main.html',
                            # Artist Metadata
                            **dynamic_vars,
                            # Graph Datapoints
                            #all_labels=all_labels,
                            past_data=past_data,
                            pred_data=pred_data,
                            
                            ncolor='rgba(50, 115, 220, 0.4)',
                            gcolor='rgba(0, 205, 175, 0.4)')               
    except Exception as e:
        print('>>> ERROR: ', e)
        return doc
    #return {"doc":doc,             "x_labels":x_labels,             "y_labels":y_values}



app.run(host="0.0.0.0", port=PORT, debug=True)