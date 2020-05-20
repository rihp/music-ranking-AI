import datetime
import pmdarima as pm
from src import config
from src.utils import clean_signal
from src.controllers import spotify_handler, chartmetric_handler

# -------------------------------------------------------- #
#                Machine Learning Models                   #
# -------------------------------------------------------- #
def predict(df, n_periods=30):
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
    # Clean the noisy signal, using a Fourier Transform / Butterworth Fitler
    #df_cleaned = clean_signal(df, Fm=365, Fc=7)
    df_cleaned = df.copy()
    # Train the model
    model_params ={"random_state":True, "suppress_warnings":True, "trace":True, "error_action":'ignore'}
    trained_model = pm.auto_arima(df_cleaned, # Data to fit to
                        seasonal=True, m=7,   # Seasonality
                        **model_params        # Debugging options
                        ) 
    """
    # Export the trained model as a pickle
    with open(f'{config.OUTPUT_models_trained_path}_CPP.pkl', 'wb') as pkl:
        pickle.dump(trained_model, pkl)
    """

    # Make a prediction.
    pred = trained_model.predict(n_periods=n_periods).round()
    return pred

# -------------------------------------------------------- #
#                    Transforming Data                     #
# -------------------------------------------------------- #
def predictions_to_json(preds_array, date_end):
    tmstp = datetime.date.fromisoformat(date_end)
    for CPPrank in preds_array:
        tmstp += datetime.timedelta(days=1)
        yield {"rank": int(CPPrank),
               "timestp": tmstp.isoformat()}
