# API ENDPOINT EXAMPLE:

### Request through a `main.py`
```
from os import get_params
from flask import (...)
from src.predictor import predict

@api.route(/api/artist/<id>/cpp-rank-prediction?days=4)
def predict_cpp(id):
    days = get_params(days)
    return predict(days)
```

### Response
```
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