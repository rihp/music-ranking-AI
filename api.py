import os
import pandas as pd
import numpy as np
from datetime import date
from flask import Flask, request, app, render_template

# My modules:
from src.config import PORT
from src.controllers import mongo_handler as mah
from src.controllers import chartmetric_handler as cmh
from src.controllers import spotify_handler as sfh
from src.predictor import predict, predictions_to_json

# Request data since this date
since="2018-01-01"

# FLASK SETUP
app = Flask(__name__)

@app.route("/")
def landing_page():
    #return home_html
    return {'message':
    f'Hello, world! Welcome to my Music Prediction API.'}

@app.route("/api/artist/<spotify_artist_id>/predict/<metric>")
def predict_artist_metric(spotify_artist_id, metric, n_periods=30, since=since, until=date.today().isoformat(), platform = 'spotify'):
    """
    Input:  A dataframe with a datetime index and the number of periods to predict
    Output: The `_id` of the created document in Mongo Atlas
    """
    # 1. Query Available data for the specified `artist_id` in all external data sources. 
    query_params = { "since":since, "until":until, "metric":metric }   
    sf_data = sfh.q_spotify(spotify_artist_id)                                      # Present data about the artist
    cm_data = cmh.q_chartmetric(platform, spotify_artist_id, **query_params)        # Historic data about the artist
    df = cm_data.copy()    
    # 2. Generate prediction with the defined models
    pred_df = predict(df, n_periods=n_periods)
    # 3. Send time-series prediction to Mongo Atlas
    preds_json = list(predictions_to_json(pred_df, until))

    message = mah.send_to_database(sf_data, preds_json, metric=metric)
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
        preds = doc['predictions']
        x_labels = [ e['timestp'] for e in preds]
        y_values = [ e['rank'] for e in preds]
        return render_template('main.html',
                            nvalues=y_values,
                            nlabels=x_labels,
                            ncolor='rgba(50, 115, 220, 0.4)')
    except: return doc
    #return {"doc":doc,             "x_labels":x_labels,             "y_labels":y_values}

@app.route("/api/chart")
def sample_report():
    n, bins = 10000, 20
    normal = np.random.normal(0, 1, n)
    gumbel = np.random.gumbel(0, 1, n)
    weibull = np.random.weibull(5, n)
    nhistogram = np.histogram(normal, bins=bins)
    ghistogram = np.histogram(gumbel, bins=bins)
    whistogram = np.histogram(weibull, bins=bins)

    return render_template('main.html',
                            nvalues=nhistogram[0].tolist(),
                            nlabels=nhistogram[1].tolist(),
                            ncolor='rgba(50, 115, 220, 0.4)',
                            gvalues=ghistogram[0].tolist(),
                            glabels=ghistogram[1].tolist(),
                            gcolor='rgba(0, 205, 175, 0.4)',
                            wvalues=whistogram[0].tolist(),
                            wlabels=whistogram[1].tolist(),
                            wcolor='rgba(255, 56, 96, 0.4)')



app.run(host="0.0.0.0", port=PORT, debug=True)