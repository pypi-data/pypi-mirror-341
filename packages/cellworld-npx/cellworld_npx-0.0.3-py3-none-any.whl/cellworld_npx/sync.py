from json_cpp import JsonObject, JsonList
from itertools import groupby
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import json
from .camera import get_roi_intensity


class DriftCoeff(JsonObject):
    def __init__(self, name=str(), coeffs=list(), matching_events=list(), error=list()):
        self.name = name
        self.coeffs = coeffs
        self.matching_events = matching_events
        self.error = error


class DriftCoeffs(JsonList):
    def __init__(self):
        super().__init__(list_type=DriftCoeff)


class SyncDevices(JsonList):
    def __init__(self):
        super().__init__(list_type=SyncDevice)


class SyncDevice(JsonObject):
    def __init__(self, full_name=str(), root=str()):
        self.full_name = full_name
        self.root = root
        self.sample_rate = int()
        self.start_sample = int()
        self.start_time = float()
        self.sync_times = list()
        self.sync_states = list()
        self.sync_samples = list()
        self.drift_coeffs = DriftCoeffs()
        self.name = self.clean_name()
        self.sync_path = self.get_sync_path()

        self.load_sync_info()
        self.get_sample_rate()


    def clean_name(self):
        if 'episode' in self.full_name:
            name = self.full_name
        else:
            string = self.full_name
            string = string.split('Start Time for ')[-1].split('@')[0]
            string = string.replace('(', '-')
            string = string.replace(')', '')
            string = string.replace(' - ', '.')
            string = string.replace(' ', '')
            name = string
        return name
    

    def get_sync_path(self):
        if 'episode' in self.name:
            sync_path = glob.glob(os.path.join(self.root, '*sync*.json'))[0]
        elif 'mp4' in self.root:
            sync_path = self.root
        else:
            sync_path = os.path.join(self.root, 'events', self.name, 'TTL')
        return sync_path

    
    def get_sample_rate(self):
        if self.sample_rate == 0:
            if 'episode' in self.name:
                if len(self.sync_times) > 0:
                    self.sample_rate = np.mean(1 / (np.diff(self.sync_times) / np.diff(self.sync_samples)))
            else:
                x = self.full_name.split('@')
                if len(x) == 2:
                    self.sample_rate = int(x[1].replace(' Hz', '').strip())


    def load_sync_info(self):
        if 'episode' in self.name:
            self.sync_times, self.sync_samples, self.sync_states = self.load_tracking_sync()
            self.start_time = 0

        elif 'camera' in self.name:
            self.sync_times, self.sync_samples, self.sync_states = self.load_entrance_sync()
            self.start_sample = 0
            self.start_time = 0

        else:
            self.start_time, self.start_sample, self.sync_times, self.sync_samples, self.sync_states = self.get_sync_times()


    def get_sync_times(self):
        sync_messages = os.path.join(self.sync_path, '..', '..', '..', 'sync_messages.txt')
        if os.path.exists(sync_messages):
            data = load_sync_messages(sync_messages)
            start_sample = data[self.full_name]
        else:
            start_sample = None
        try:
            sync_times = np.load(os.path.join(self.sync_path, 'timestamps.npy'))
            start_time = sync_times[0]
        except:
            sync_times = None
            start_time = None
        try:
            sync_states = np.load(os.path.join(self.sync_path, 'states.npy'))
        except:
            sync_states = None
        try:
            sync_samples = np.load(os.path.join(self.sync_path, 'sample_numbers.npy'))
        except:
            sync_samples = None
        return start_time, start_sample, sync_times, sync_samples, sync_states
    

    def load_entrance_sync(self, ROI=(224, 351, 10, 14), threshold=None):
        led_values, self.sample_rate = get_roi_intensity(self.sync_path, ROI=ROI)
        if threshold is None:
            threshold = np.std(led_values - np.mean(led_values))
        led_signal = (led_values > threshold).astype(int)
        # discard first 10 or so frames... wait for sensor to stabilize
        led_signal[0:10] = 0
        dff = np.diff(led_signal)
        samples = np.argwhere(dff != 0).squeeze()
        states = dff[samples]
        return samples / self.sample_rate, samples, states


    def load_tracking_sync(self):
        with open(self.sync_path) as f:
            data = json.load(f)
        try:
            # get first led state change across the four cameras
            ts = data['time_stamps']
            state = np.vstack(data['leds']) 
            state_change = np.sum(np.diff(state, axis=0), axis=1) > 0
            state_idx = np.array([list(g)[0]+1 for k,g in groupby(range(len(state_change)), lambda idx:state_change[idx])])
            sync_state = state_change[state_idx-1].astype(int)
            sync_state[sync_state == 0] = -1
            sync_state[sync_state == 1] = 1
            sync_times = np.array(ts)[state_idx]
            sync_frames = np.array(data['frames'])[state_idx]
        except:
            print('No sync data found')
            sync_times = []; sync_frames = []; sync_state = []

        return sync_times, sync_frames, sync_state


    def get_events(self, state=None):
        if 'episode' in self.name or 'camera' in self.name:
            # return raw times for behavioral data
            ts = self.sync_times; states = self.sync_states
        else:
            # return seconds from start for neural data
            ts = (self.sync_samples - self.start_sample) / self.sample_rate; states = self.sync_states
        if state is not None:
            assert state in np.unique(states), f'state {state} not found in SyncDevice'
            return ts[states == state]
        else:
            return ts, states
        

    def get_event_durations(self, state=1, return_events=True):
        on, off = clean_events(self.get_events(state=state), self.get_events(state=-state))
        if 'camera' in self.name:
            # include only the first run of correct events
            I = np.argwhere((np.diff(on) > 1.1) | (np.diff(on) < 0.9)).squeeze()[0]
            on = np.round(on[:I],1); off = np.round(off[:I],1)
        else:
            [on, off] = remove_bad_onsets([on, off], dt=0.9)
        # if 'camera' not in self.name:
        #     [on, off] = remove_bad_onsets([on, off], dt=0.9)
        if return_events:
            return off - on, [on, off]
        else:
            return off - on
        

    def align(self, device, states=[1,1], err_threshold=None, return_err=False, plot_err=False):
        x_dt, x_ev = self.get_event_durations(state=states[0])
        y_dt, y_ev = device.get_event_durations(state=states[1])

        # check sequence lengths and find matching events
        flag = False
        x_ind, y_ind, err = match_event_lag(x_dt, y_dt)
        if err_threshold is None:
            err_threshold = np.median(err) - 6*np.std(err)
        if plot_err:
            plt.plot(err,'.')
            plt.axhline(err_threshold, color='r', linestyle='--')
            if np.min(err) <= err_threshold:
                plt.plot(y_ind[0], err[y_ind[0]], 'ro', zorder=-1) 
            plt.xlabel('Lag'); plt.ylabel('Error')
        if np.min(err) > err_threshold:
            flag = True
            print(f'failed to match {self.name} events to {device.name} events, err > {err_threshold} ({np.min(err)})')
            #assert np.min(err) < min_err, f'failed to match {self.name} events to {device.name} events, err > {min_err} ({np.min(err)})'
        x_syncs = x_ev[0][x_ind]
        y_syncs = y_ev[0][y_ind]
        if len(x_syncs) != len(y_syncs):
            flag = True
            print(f'could not match {len(x_syncs)} {self.name} events to {len(y_syncs)} {device.name} events')
            #assert len(x_syncs) == len(y_syncs), f'Could not match {len(x_syncs)} {self.name} events to {len(y_syncs)} {device.name} events'

        if not flag:
            b = fit_drift(x_syncs, y_syncs)
            self.drift_coeffs.append(DriftCoeff(f'{self.name}->{device.name}', b, [x_ind, y_ind], err))
        else:
            self.drift_coeffs.append(DriftCoeff())

        if return_err:
            return err, x_ind, y_ind
        
        
    
def load_sync_messages(file):
    with open(file) as f:
        lines = f.readlines()
        data = {}
        for line in lines:
            l = line.split(':')
            data[l[0]] = int(l[1].strip())
    return data

def fit_drift(x, y):
    assert len(x) == len(y), f"x (len {len(x)}) must be the same length as y (len {len(y)}))"
    z = np.polyfit(x, y, 1)
    return z

def clean_events(on_ev, off_ev):
    # if signal started high, discard first off event
    if off_ev[0] < on_ev[0]:
        off_ev = np.delete(off_ev, 0)

    # if signal ended high, discard last on event
    if off_ev[-1] < on_ev[-1]:
        on_ev = np.delete(on_ev, -1)

    return on_ev, off_ev

def match_event_lag(a, b):
    if len(a) > len(b):
        lag, mid, err = lag_shift_err(a, b)
        a_ind = range(lag-mid, lag+mid+1)
        b_ind = range(0, len(b))
    else:
        lag, mid, err = lag_shift_err(b, a)
        a_ind = range(0, len(a))
        b_ind = range(lag-mid, lag+mid+1)
    if (len(a_ind) - len(b_ind)) == 1:
        a_ind = a_ind[:-1]
    if (len(b_ind) - len(a_ind)) == 1:
        b_ind = b_ind[:-1]
    return a_ind, b_ind, err

def lag_shift_err(a, b):
    '''
    Matches the values of two event traces by lagging them in time and finding the lowest error.
    a:   event durations from source a
    b:   event durations from source b
    lag, mid, error: returns the lag with the lowest error, the midpoint, and the error vector
    '''
    mid = int(np.floor(len(b)/2))
    add = len(b) % 2
    lags = []
    err = []
    for l in range(len(a)):
        if (l >= mid) & (l <= (len(a)-mid-add)):
            err.append(np.linalg.norm(b - a[l-mid:l+mid+add]))
            lags.append(l)
    assert len(err) > 0, f'error must not be empty... len(err) = {len(err)}'
    return lags[np.argmin(err)], mid, err

def match_sync_lag(a, b):
    '''
    Matches the values of two event traces by lagging them in time and finding the lowest error.
    Will return None, None if error is greater than one
    a:   event durations from source a
    b:   event durations from source b
    returns: the common index of the two event traces
    '''
    # the longer of the two is "A"
    if len(b) > len(a):
        A = b
        B = a
    else:
        A = a
        B = b

    # lag match A and B
    lag, mid, err = lag_shift_err(A, B)
    if np.min(err) > 1:
        return None, None 
    return range(lag-mid, lag+mid), range(lag-mid, lag+mid)

def lag_shift_err_full(a, b, return_error=False):
    '''
    Matches the duration of two event traces by lagging them in time and finding the lowest error.
    This is slightly different than lag_shift_err, in that it performs a full convolution of the two vectors.
    Will return None, None if error is greater than one
    a:   event durations from source a
    b:   event durations from source b
    returns: the indices of matching elements of a and b, and the error
    '''
    def erf(a, b, l, verbose=False, plot=False):
        '''
        computes error at given lag
        a, b: signal a and b (len(b) < len(a))
        l: lag index [0:len(a)+len(b)]
        '''
        if l < len(b):
            ai = range(0, l+1)
            bi = range(len(b)-l-1, len(b))
            if plot:
                plt.plot(a, 'tab:blue', alpha=0.5)
                plt.plot(range(0,l+1), b[bi], 'o', color='tab:orange')
                plt.plot(a[ai], '.', color='tab:blue')
                plt.plot(range(-len(b)+l+1,l+1), b, 'tab:orange', alpha=0.5)
                plt.xlim([-5,l+5])
                plt.title('b before a')
        elif (l >= len(b)) & (l <= len(a)):
            ai = range(l-len(b), l)
            bi = range(0, len(b))
            if plot:
                plt.plot(a, 'tab:blue', alpha=0.5)
                plt.plot(range(l-len(b), l), b[bi], 'o', color='tab:orange')
                plt.plot(range(l-len(b), l), a[ai], '.', color='tab:blue')
                plt.title('b in a')
        elif l >= (len(a)):
            ai = range(len(a)-len(b) + l-len(a), len(a))
            bi = range(0, (l - len(a) - len(b)) * -1)
            if plot:
                plt.plot(a, 'tab:blue', alpha=0.5)
                plt.plot(range(len(a)-len(b) + l-len(a), len(a)), b[bi], 'o', color='tab:orange')
                plt.plot(range(len(a)-len(b) + l-len(a), len(a)), a[ai], '.', color='tab:blue')
                plt.title('b after a')
        
        e = np.linalg.norm(b[bi]-a[ai])
        if verbose:
            print(l, len(ai),len(bi), e)
        
        return ai, bi, e

    a = np.round(a*10)/10
    b = np.round(b*10)/10
    err = []
    for l in range(len(a) + len(b)):
        ai, bi, e = erf(a,b,l)
        err.append(e)
    [ai, bi, e] = erf(a,b,np.argmax(np.diff(err)))
    if return_error:
        return ai, bi, err
    return ai, bi, e


def remove_extra_events(*args, dt = 1):
    '''
    Removes events that fall under a specific inter-event time (dt)
    args:   args are the events you want to remove from, with the first argument being 
            the vector to search for extra events in
    dt:     the time delay between events, if an event falls below this it will
            be removed
    '''
    X = list(args)
    extra = np.argwhere(np.diff(X[0]) < dt).squeeze()
    print(extra)
    if len(extra) > 0:
        X_out = []
        extra = extra[0]+1
        for x in X:
            X_out.append(np.delete(x, extra))
        return [x for x in X_out]
    else:
        return [x for x in X]
    
def remove_bad_onsets(X, dt=0.9):
    bad_onsets = np.argwhere(np.diff(X[0]) < dt)
    while len(bad_onsets) > 0:
        X_out = []
        for x in X:
            X_out.append(np.delete(x, bad_onsets[0]+1))
        X = X_out
        bad_onsets = np.argwhere(np.diff(X[0]) < dt)
    return X