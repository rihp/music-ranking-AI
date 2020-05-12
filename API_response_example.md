# Artist ranking predictor.
## Supervised Machine Learning

Using a time series of artist ranking, from established data sources like [`Chartmetric API`](https://api.chartmetric.com/apidoc/#api-Artist-GetArtistCPP) or [`Spotify Api`](https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-flows).

Consider the use of **Reinforcement Learning**; as time goes by, the model will learn to return more accurate predictions.

# API ENDPOINT EXAMPLE:

### HTTP Endpoint from our `api.py`
```python
from os import get_params
from flask import app
(...)
from src.predictor import predict

@app.route(/api/artist/<id>/cpp-rank-prediction?days=4)
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
        },
        {
            "spotify_id": 6970440,
            "predicted_rank": 3,
            "confidence":0.85 ,
            "timestp": "2019-06-07T07:00:00.000Z"
        },
        {
            "spotify_id": 6970440,
            "predicted_rank": 1,
            "confidence":0.65 ,
            "timestp": "2019-06-06T07:00:00.000Z"
        }
    ]
}
```

### Possible graphic representation of the data:

![Delta-time and overall artist rank.](/INPUT/basic_data_points.png)

![Prediction representation](/INPUT/compare_prediction_gt.png)