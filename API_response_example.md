# Artist ranking predictor.
## Supervised Machine Learning

Using a time series of artist ranking, from established data sources like:
- [`Chartmetric API`](https://api.chartmetric.com/apidoc/#api-Artist-GetArtistCPP)
- [`Spotify API`](https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-flows) | [`Spotify Developer Access`](https://developer.spotify.com/) | [`Spotify Search`](https://developer.spotify.com/documentation/web-api/reference/search/search/)
- [`iTunes Search API`](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/UnderstandingSearchResults.html#//apple_ref/doc/uid/TP40017632-CH8-SW1) | [`iTunes Music Charts`](https://developer.apple.com/documentation/applemusicapi/get_catalog_charts) | [`Create Apple Developer Token`](https://developer.apple.com/documentation/applemusicapi/getting_keys_and_creating_tokens)

Consider the use of **Reinforcement Learning**; as time goes by, the model will learn to return more accurate predictions.

# API ENDPOINT EXAMPLE:

### HTTP Endpoint from our `api.py`
```python
from os import get_params
from flask import app
(...)
from src.predictor import predict

# Artist - Predict CPP (Cross-Platform Performance)
@app.route(/api/artist/<id>/cpp-rank-prediction?days=2)
def predict_cpp(id):
    days = get_params(days)
    return predict(days)
```

### HTTP Response
```json
 {
    "obj": [
        {
            "spotify_id": 6970440,
            "predicted_rank": 4,
            "confidence":0.95 ,
            "timestp": "2019-06-09T07:00:00.000Z"
        },
        {
            "spotify_id": 6970440,
            "predicted_rank": 3,
            "confidence":0.75 ,
            "timestp": "2019-06-08T07:00:00.000Z"
        }
    ]
}
```

### Possible graphic representation of the data (MVP):
Considering only the ground truth, plot behavior of the artist ranking vector on `matlotlib`:

##### Evolution of artist ranking metric over time. 
![Delta-time and overall artist rank.](/INPUT/basic_data_points.png)

##### Comparing our predictions with the `Ground Truth`.
![Prediction representation](/INPUT/compare_prediction_gt.png)


### More possible implementations:
Include a comparison of different machine learning models and their prediction metrics.

![Prediction Models Compared](/INPUT/2013Ma_Sun_Cong.png)

- Enrich dataframes with `Twitter API` requests, analyzed by the `Google Cloud Natural Language API` [1](https://cloud.google.com/natural-language) | [API](https://cloud.google.com/natural-language/docs/reference/rest/?apix=true) | [Languages supported](https://cloud.google.com/natural-language/docs/languages)

### HTTP Response (Multiple models)
```json
 {
    "obj": [
        {
            "spotify_id": 6970440,
            "predictions": [{
                        "spotify_id": 6970440,
                        "predicted_rank": 1,
                        "model": "H2O_AutoML",
                        "confidence":0.85 ,
                        "timestp": "2019-06-06T07:00:00.000Z"
                        },
                        {
                        "spotify_id": 6970440,
                        "predicted_rank": 2,
                        "model": "linear_regressor",
                        "confidence":0.76 ,
                        "timestp": "2019-06-06T07:00:00.000Z"
                        },
                        {
                        "spotify_id": 6970440,
                        "predicted_rank": 2,
                        "model": "GradientBoostingRegressor",
                        "confidence":0.42 ,
                        "timestp": "2019-06-06T07:00:00.000Z"
                        }       
                    ]  
                }
            ]
        }
    ]
}
```

### Bonus (Exposure & Portfolio):
- Send a tweet when a new prediction is made for an specified `artist_id`
- Generate a docker image
- Deploy to Heroku