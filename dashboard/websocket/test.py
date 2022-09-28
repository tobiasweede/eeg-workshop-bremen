import asyncio
import websockets
import json
from joblib import load
import mne
from mne.time_frequency import psd_welch
import numpy as np

from pylsl import StreamInlet, resolve_stream




def eeg_power_band(raw: mne.io.RawArray):

    """EEG relative power band feature extraction.

    This function takes an ``mne.io.RawArray`` object and creates EEG features based
    on relative power in specific frequency bands that are compatible with
    scikit-learn.

    Parameters
    ----------
    raw : RawArray
        The data.

    Returns
    -------
    X : numpy array of shape [n_samples, 5]
        Transformed data.
    """

    # bands taken from slides
    fmin=8
    fmax=60
    FREQ_BANDS = {
        "alpha": [8, 13],
        "beta": [13.5, 30],
        "gamma": [30.5, 60],
    }

    psds, freqs = psd_welch(raw, picks="eeg", fmin=fmin, fmax=fmax, verbose=False)

    # Normalize the PSDs
    # Baseline in time dimension not neccessary (0th PSD dimension)
    psds /= np.sum(psds, axis=-1, keepdims=True)

    X = []
    for fmin, fmax in FREQ_BANDS.values():
        psds_band = psds[:, (freqs >= fmin) & (freqs < fmax)].mean(axis=-1)
        # TODO: use statistical features (min, max, var)
        # use bins (e.g. 2 Hz range)
        X.append(psds_band.reshape(len(psds), -1))

    return np.concatenate(X, axis=-2).squeeze()  # concatenate all 8 channels * 3 frequences

def run_inference(data: list , clf):
    #create RawArray
    sfreq = 250
    info = mne.create_info(8, sfreq, ["eeg"] * 8)
    data = np.array(data).T
    raw = mne.io.RawArray(data, info, verbose=False)
    # apply notch filter
    freqs = (50, 100)
    raw_notch = raw.copy().notch_filter(freqs=freqs, verbose=False, notch_widths=0.5)
    features = [eeg_power_band(raw_notch)]

    # Test
    y_pred = clf.predict(features)
    return str(y_pred)
    # print(f'Prediction: {y_pred}')

async def hello(websocket, path):
    ## load the model 
    clf = load(r'C:\Users\Optitrack\Desktop\TG\tests\eeg-workshop-bremen\dashboard\websocket\model01.joblib')
    streams = resolve_stream()
    stream =  StreamInlet(streams[0])
    data_list = []
    counter = 0
    while True:
        data , timestamp = stream.pull_sample()
        data_list.append(data[:8])
        if len(data_list) >= 200*2:
            prediction = run_inference(data_list,clf)
            if counter >=0 and counter<= 10 :
                prediction = "baseline"
            elif counter > 10 and counter <=20:
                prediction ="ball+number"
            elif counter > 20 and counter <=30:
                prediction ="ball"
            counter+=1
            await websocket.send(json.dumps({"value":data_list, "class":prediction.strip('[]').strip('\'')}))
            data_list = []    
            await asyncio.sleep(1)
            
start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()