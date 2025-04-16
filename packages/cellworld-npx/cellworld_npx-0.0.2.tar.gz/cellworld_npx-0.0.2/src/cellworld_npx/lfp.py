from matplotlib.colors import TwoSlopeNorm
from kilosort.io import BinaryFiltered, load_ops
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from torch.fft import fft, ifft, fftshift
from .probe import channel_to_lfp
from .io import walk_back, find_file
from tqdm import tqdm
import numpy as np
import torch
import os


def get_binary_file(binary_file, return_ops=False, 
                    hp_filter=False, whiten=False, dshift=False):
    device = torch.device('cuda')
    binary_file, ops_file = find_binary_file(binary_file)
    ops = load_ops(ops_file)
    chan_map = ops['chanMap']
    if hp_filter:
        hp_filter = ops['fwav']
    else:
        hp_filter = None
    if whiten:
        whiten = ops['Wrot']
    else:
        whiten = None
    if dshift:
        dshift = ops['dshift']
    else:
        dshift=None
    bfile = BinaryFiltered(binary_file, n_chan_bin=ops['n_chan_bin'], 
                           chan_map=chan_map, device=device,
                           hp_filter=hp_filter, 
                           whiten_mat=whiten, 
                           dshift=dshift)
    if return_ops:
        return bfile, ops
    else:
        return bfile
    
def find_binary_file(binary_file):
    if 'continuous.dat' in binary_file:
        pass
    elif 'continuous.dat' in os.listdir(binary_file):
        binary_file = Path(binary_file) / 'continuous.dat'
    else:
        root_path = walk_back(binary_file, 'Record Node')
        binary_file = find_file(root_path, 'continuous.dat', joined=True)
        assert binary_file is not None, f'continuous.dat not found in {binary_file}'
        assert len(binary_file) == 1, f'multiple continuous.dat files found in {binary_file}, check your folder structures'
        binary_file = binary_file[0]
    ops_file = find_file(os.path.split(binary_file)[0], 'ops.npy', joined=True)
    if ops_file is None:
        # if ops.npy is not in the binary path, look backwards for it
        root_path = walk_back(binary_file, 'Record Node')
        ops_file = find_file(root_path, 'ops.npy', joined=True)
        assert ops_file is not None, f'no ops.npy file found, run kilosort'
        assert len(ops_file) == 1, f'{len(ops_file)} ops.npy files found, requires a single file'
    ops_file = ops_file[0]
    return binary_file, ops_file
    
def get_spike_amplitudes(results_dir):
    # calculate or load spike amplitudes
    results_dir = Path(results_dir)
    fn = results_dir / 'spike_amplitudes.npy'
    if not fn.exists():
        bfile = get_binary_file(results_dir)
        spike_times = np.load(results_dir / 'spike_times.npy')
        ops = load_ops(results_dir / 'ops.npy')
        spike_amps = np.zeros((len(spike_times), ops['n_chan_bin']))
        for i,t in enumerate(tqdm(spike_times), desc='extracting spike amplitudes'):
            tmin = t - bfile.nt0min
            tmax = t + (bfile.nt - bfile.nt0min) + 1
            spike_amps[i,:] = bfile[tmin:tmax].cpu().numpy()[:,ops['nt0min']].astype('float32')
        np.save(fn, spike_amps)
    else:
        print(f'loading spike amplitudes from {fn}')
        spike_amps = np.load(fn)

    return spike_amps

def get_filter(cutoff, fs=30000, device=torch.device('cuda'), btype='highpass', order=1):
    if type(cutoff) is list:
        btype = 'bandpass'
    
    # a butterworth filter is specified in scipy
    b,a = butter(order, cutoff, fs=fs, btype=btype)

    # a signal with a single entry is used to compute the impulse response
    NT = 30122
    x = np.zeros(NT)
    x[NT//2] = 1

    # symmetric filter from scipy
    filter = filtfilt(b, a, x).copy()
    filter = torch.from_numpy(filter).to(device).float()
    return filter

def filter_to_fft(filter, NT=30122):
    """Convert filter to fourier domain."""
    device = filter.device
    ft = filter.shape[0]

    # the filter is padded or cropped depending on the size of NT
    if ft < NT:
        pad = (NT - ft) // 2
        fhp = fft(torch.cat((torch.zeros(pad, device=device), 
                             filter,
                             torch.zeros(pad + (NT-pad*2-ft), device=device))))
    elif ft > NT:
        crop = (ft - NT) // 2 
        fhp = fft(filter[crop : crop + NT])
    else:
        fhp = fft(filter)
    return fhp

def fft_filter(filter, X):
    fwav = filter_to_fft(filter, NT=X.shape[-1])
    X = torch.real(ifft(fft(X) * torch.conj(fwav)))
    X = fftshift(X, dim = -1)
    return X

def filter_torch(x, cutoff, btype='highpass', fs=30000, device=torch.device('cuda'), order=1):
    filter = get_filter(cutoff=cutoff, fs=fs, btype=btype, device=device, order=order)
    return fft_filter(filter, x)

def numpy_to_torch(data):
    if type(data) is np.ndarray:
        if torch.cuda_is_available():
            data = torch.from_numpy(data).to('cuda')
        else:
            data = torch.from_numpy(data).to('cpu')
    return data

def rms_torch(data):
    data = numpy_to_torch(data)
    return torch.sqrt(torch.sum(torch.square(data), axis=-1) / data.shape[1])

def hilbert_torch(data):
    data = numpy_to_torch(data)
    transforms = -1j * torch.fft.rfft(data, axis=-1)
    transforms[0] = 0
    imaginary = torch.fft.irfft(transforms, axis=-1)
    real = data
    return torch.complex(real, imaginary)

def plot_lfp(arr, times=[], offset=100, heat_map=False, fs=30e3, ax=plt, bounds=None, yvals=None, scale=1, 
             color='k', alpha=0.5, linewidth=0.5, **kwargs):
    if type(arr) is torch.Tensor:
        arr = arr.cpu()
    if len(arr.shape) == 1:
        arr = arr[np.newaxis,:]
    if len(times) == 0:
        rng = range(0,arr.shape[1])
    else:
        rng = range(int(np.round(times[0]*fs)),
                int(np.round(times[1]*fs)))
    t = np.array(rng) / fs
    plt_dat = arr[:,rng] * scale

    if not heat_map:
        if yvals is not None:
            yvals = np.array(yvals)
            if len(yvals.shape) == 0:
                yvals = np.array([yvals])
            plt_dat += yvals[:,np.newaxis]
        else:
            plt_offsets = np.arange(0, plt_dat.shape[0]*offset, offset)
            plt_dat += plt_offsets[:,np.newaxis]
        _ = ax.plot(t, plt_dat.T, color=color, alpha=alpha, linewidth=linewidth, **kwargs)
    else:
        if bounds is not None:
            if len(bounds) == 1:
                vmin = bounds[0]
                vmax = bounds[0]
            elif len(bounds) == 2:
                vmin = bounds[0]
                vmax = bounds[1]
        else:
            vmin = None
            vmax = None
        h = ax.pcolor(t, np.arange(plt_dat.shape[0]), plt_dat, cmap='coolwarm', norm=TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax), rasterized=True)
        plt.colorbar(h, label='uV')

def gaussian(x, mu=0, sd=1):
    return 1.0 / (np.sqrt(2.0 * np.pi) * sd) * np.exp(-np.power((x - mu) / sd, 2.0) / 2)

def gaussian_kernel(sd=1, width=None):
    if width is None:
        width = int(sd*6)
    t = np.linspace(-width, width, width*2+1)
    return gaussian(t, sd=sd)

def gaussian_smoother(x, sd=1, width=None):
    return np.convolve(x, gaussian_kernel(sd=sd, width=width), 'same')

def gaussian_filter_torch(x, sd=1, width=None):
    kernel = gaussian_kernel(sd=sd, width=width)
    kernel = torch.from_numpy(kernel).to('cuda') 
    kernel = kernel.view(1, 1, 1, -1).float()
    x = x.expand(1, 1, x.shape[0], -1)
    return torch.conv2d(x, kernel, padding="same").squeeze()

def get_ripple_amplitude(x, sd=0.004, fs=30000, method='sum'):
    if 'each' in method:
        x_ripple = filter_torch(x, [100, 250], order=1)
        amplitude = hilbert_torch(x_ripple).abs() # abs of hilbert transform to get amplitude
        amplitude = gaussian_filter_torch(amplitude, sd=int(sd*fs)) # smooth
        amplitude = ((amplitude.T - amplitude.mean(1)) / amplitude.std(1)).T # z-score
    elif 'sum' in method:
        x_ripple = filter_torch(x, [150, 250], order=1)
        amplitude = (x_ripple ** 2).sum(0).expand(1,-1) # power is square and sum over supplied channels
        amplitude = gaussian_filter_torch(amplitude, sd=int(sd*fs)) ** 0.5 # smooth and sqrt
        amplitude = (amplitude - amplitude.mean()) / amplitude.std() # z-score
    return amplitude.cpu().numpy()

def get_amplitude(x, sd=0.004, fs=30000, band=[6,12], method='each'):
    x_f = filter_torch(x, band, order=1)
    if (method == 'sum') & (len(x.shape) > 1):
        amplitude = (x_f ** 2).sum(0)
    else:
        amplitude = (x_f ** 2)
    if len(amplitude.shape) == 1:
        amplitude = amplitude.expand(1,-1)
    if sd > 0:
        amplitude = gaussian_filter_torch(amplitude, sd=int(sd*fs)) ** 0.5
    if len(amplitude.shape) > 1:
        amplitude = (amplitude.T - amplitude.mean(1)) / amplitude.std(1).T
    else:
        amplitude = (amplitude - amplitude.mean()) / amplitude.std()

    return amplitude.cpu().numpy()

def get_rms_amplitude(x, band=[6,12]):
    x_f = filter_torch(x, band, order=1)
    return torch.sqrt(torch.mean(x_f**2, axis=1)).cpu().numpy()


# def load_binary_chunk(dp, times, channels=np.arange(384), filt_key='lowpass', scale=True, verbose=False):
#     dp = Path(dp)
#     meta = read_metadata(dp)
#     fname = Path(dp)/meta[filt_key]['binary_relative_path'][2:]
    
#     fs = meta[filt_key]['sampling_rate']
#     Nchans=meta[filt_key]['n_channels_binaryfile']
#     bytes_per_sample=2
    
#     assert len(times)==2
#     assert times[0]>=0
#     assert times[1]<meta['recording_length_seconds']
    
#     # Format inputs
#     ignore_ks_chanfilt = True
#     channels=assert_chan_in_dataset(dp, channels, ignore_ks_chanfilt)
#     t1, t2 = int(np.round(times[0]*fs)), int(np.round(times[1]*fs))
    
#     vmem=dict(psutil.virtual_memory()._asdict())
#     chunkSize = int(fs*Nchans*bytes_per_sample*(times[1]-times[0]))
#     if verbose:
#         print('Used RAM: {0:.1f}% ({1:.2f}GB total).'.format(vmem['used']*100/vmem['total'], vmem['total']/1024/1024/1024))
#         print('Chunk size:{0:.3f}MB. Available RAM: {1:.3f}MB.'.format(chunkSize/1024/1024, vmem['available']/1024/1024))
#     if chunkSize>0.9*vmem['available']:
#         print('WARNING you are trying to load {0:.3f}MB into RAM but have only {1:.3f}MB available.\
#               Pick less channels or a smaller time chunk.'.format(chunkSize/1024/1024, vmem['available']/1024/1024))
#         return
    
#     # Get chunk from binary file
#     with open(fname, 'rb') as f_src:
#         # each sample for each channel is encoded on 16 bits = 2 bytes: samples*Nchannels*2.
#         byte1 = int(t1*Nchans*bytes_per_sample)
#         byte2 = int(t2*Nchans*bytes_per_sample)
#         bytesRange = byte2-byte1

#         f_src.seek(byte1)

#         bData = f_src.read(bytesRange)
        
#     # Decode binary data
#     # channels on axis 0, time on axis 1
#     assert len(bData)%2==0
#     rc = np.frombuffer(bData, dtype=np.int16) # 16bits decoding
#     rc = rc.reshape((int(t2-t1), Nchans)).T
#     rc = rc[channels, :]
    
#     # Scale data
#     if scale:
#         rc = rc * meta['bit_uV_conv_factor'] # convert into uV
    
#     return rc