from IPython.display import Audio, display
import datetime

def makesound(sound_key):
    """ Plays the sound file of a given dictionary key """
    sounds = {
        'coin':"https://sound.peal.io/ps/audios/000/007/926/original/334298__sojan__coinflic4.mp3",
        'rick':'https://sound.peal.io/ps/audios/000/000/537/original/woo_vu_luvub_dub_dub.wav',
        'error':'https://sound.peal.io/ps/audios/000/005/602/original/youtube.mp3',
        'error2':'http://peal.io/download/uv0rk',
    }
    # Play the sound
    display(Audio(url=sounds[sound_key], autoplay=True))


def isotime(brackets=True):
    if brackets:  return f"[{datetime.datetime.today().isoformat(timespec='minutes')}]"
    else:         return datetime.datetime.today().isoformat(timespec='minutes')

def new_high_score():
    print(f"{isotime()} - \n  QUICK! MORTY! GET THE LASER GUN MORTY!\n THE MACHINE HAS LEARNED TO GENERALIZE")
    display(Audio(url='https://sound.peal.io/ps/audios/000/017/264/original/youtube_17264.mp3', autoplay=True))
