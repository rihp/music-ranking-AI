import datetime
import pmdarima as pm
from src import config
from src.utils import clean_signal
from src.controllers import spotify_handler, chartmetric_handler

# -------------------------------------------------------- #
#                Machine Learning Models                   #
# -------------------------------------------------------- #
def predict(df, n_periods=None, seasonality=None, fft=True):
    """
    INPUT: A dataframe with a datetime index
    OUTPUT: The prediction, as a new dataframe with a datetime index
    """
    """ 
    # ♠ Optimization: Consider clustering artists and saving the generated models for each type of cluster.
    try:
        with open(f'{config.OUTPUT_models_trained_path}_CPP.pkl', 'rb') as pkl:
            trained_model = pickle.load(pkl)
        print('This model has been trained before, we have successfully loaded a the model from memory!')

    except:
        print('The model has not been trained before, so we will use auto_arima to train it again')
    """ 
    # Cleaning the noisy signal, using a Fourier Transform / Butterworth Fitler
    if fft: clean_df = clean_signal(df, Fm=30, Fc=7)
    else:   clean_df = df.copy()

    clean_df.sort_index(inplace=True)
    print(f"{clean_df.head()=}")

    # Train the model
    model_params ={"random_state":True, "suppress_warnings":True, "trace":True, "error_action":'ignore'}
    trained_model = pm.auto_arima(clean_df,    # Data to fit to
                        seasonal=True,         # Seasonality
                        m=seasonality,         # moving window?
                        **model_params         # Debugging options
                        ) 
    """
    # Export the trained model as a pickle
    with open(f'{config.OUTPUT_models_trained_path}_CPP.pkl', 'wb') as pkl:
        pickle.dump(trained_model, pkl)
    """
    # Make a prediction.
    pred_df = trained_model.predict(n_periods=n_periods).round()
    print(f"{pred_df[0]=}")

    return clean_df, pred_df

# -------------------------------------------------------- #
#                    Transforming Data                     #
# -------------------------------------------------------- #
def predictions_to_json(preds_array, date_end):
    tmstp = datetime.date.fromisoformat(date_end)
    for value in preds_array:
        tmstp += datetime.timedelta(days=1)
        yield {"x": tmstp.isoformat()[:10],
               "y": int(value),}

def clean_df_to_json(clean_df):
    try:
        for tmstp, value in clean_df.iterrows():
            yield {"x": tmstp.isoformat()[:10],
                   "y": int(value),}
    except:
        for tmstp, value in clean_df.iteritems():
            yield {"x": tmstp.isoformat()[:10],
                   "y": int(value),}