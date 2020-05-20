import datetime
import pandas as pd
import numpy as np
from IPython.display import Audio, display
from scipy import signal

#   Welcome to my toolbox; 
#   
#   I hope this tiny scripts help you develop your own 
# projects. This module is intended to be verstile and easy
# to use.

# -------------------------------------------------------- #
#                   Signal Processing                      #
# -------------------------------------------------------- #
def clean_signal(noisy_signal, Fm=365, Fc=7):
    """
    Butterworth filter that cleans a signal o timeseries.
    Returns a pandas series.
    """
    Wn =Fc/Fm
    b, a = signal.butter(3, Wn)
    clean_signal = pd.Series(signal.filtfilt(b, a, np.ravel(noisy_signal.values)), index=noisy_signal.index)
    return clean_signal

# -------------------------------------------------------- #
#                         Time                             #
# -------------------------------------------------------- #
def isotime(brackets=True):
    if brackets:  return f"[{datetime.datetime.today().isoformat(timespec='minutes')}]"
    else:         return datetime.datetime.today().isoformat(timespec='minutes')

# -------------------------------------------------------- #
#                     API formatting                       #
# -------------------------------------------------------- #
def format_qparams(qparams):
    qparams_formatted = []
    for k,v in qparams.items():
        qparams_formatted.append(f"{k}={v}")
    return '&'.join(qparams_formatted)

def no_spaces(string):
    return string.replace(' ', '_')

# -------------------------------------------------------- #
#                        Sounds                            #
# -------------------------------------------------------- #
def new_high_score():
    print(f"{isotime()} - \n  QUICK! MORTY! GET THE LASER GUN MORTY!\n THE MACHINE HAS LEARNED TO GENERALIZE")
    display(Audio(url='https://sound.peal.io/ps/audios/000/017/264/original/youtube_17264.mp3', autoplay=True))

def makesound(sound_key):
    """ Plays the sound file of a given dictionary key """
    sounds = {
        'coin':"https://sound.peal.io/ps/audios/000/007/926/original/334298__sojan__coinflic4.mp3",
        'rick':'https://sound.peal.io/ps/audios/000/000/537/original/woo_vu_luvub_dub_dub.wav',
        'error':'https://sound.peal.io/ps/audios/000/005/602/original/youtube.mp3',
    }
    # Play the sound
    display(Audio(url=sounds[sound_key], autoplay=True))