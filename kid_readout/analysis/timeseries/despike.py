import random
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import filters
import scipy.signal
from kid_readout.analysis.timeseries.fftfilt import fftfilt


def lpf256(ts):
    return fftfilt(scipy.signal.firwin(256,1/256.),ts)


def medmadmask(ts,thresh=8,axis=0):
    med = np.median(ts,axis=axis)
    deviations = np.abs(ts-med)
    mad = np.median(deviations,axis=axis)
    mask = deviations > thresh*mad
    return mask


def deglitch_block(ts,thresh=5):
    tsl = np.roll(np.abs(fftfilt(scipy.signal.firwin(16,1/16.),ts)),-8)
    mask = medmadmask(tsl,thresh=thresh)
    mask[:-50] = mask[:-50] | mask[50:]
    mask[50:] = mask[50:] | mask[:-50]
    nmask = mask.sum()
#    print "rejecting",nmask/float(ts.shape[0])
    out = ts.copy()
    try:
        out[mask] = np.array(random.sample(ts[~mask],nmask))
    except ValueError:
        print "more masked values than samples to draw from!"    
    return out


def deglitch_window(data, window_length, thresh=6):
    out = np.empty_like(data)
    step = window_length//2
    nstep = data.shape[0]//step
    if nstep == 0:
        nstep = 1
    for k in xrange(nstep):
        start = k-1
        if start < 0:
            start = 0
#        print start*step,(k+1)*step,
        chunk = data[start*step:(k+1)*step]
        res = deglitch_block(chunk,thresh=thresh)
        out[start*step:((start+1)*step)] = res[:step]
    out[start*step:start*step + len(res)] = res
    return out


#the following takes up way too much memory and time, no good.
def despike_full(data, window_length, rejection_threshold=7, preprocess_function=lpf256):
    preproc = np.abs(lpf256(data))
    medians = filters.median_filter(preproc, window_length)
    abs_deviations = np.abs(preproc - medians)
    mads = filters.median_filter(abs_deviations, window_length)
    spike_flags = abs_deviations > (mads*rejection_threshold)
    nspikes = spike_flags.sum()
    data[spike_flags] = np.array(random.sample(data[~spike_flags],nspikes))
    return data


def deglitch_mask_block_mad(ts,thresh=5,mask_extend=50,debug=False):
    """

    Parameters
    ----------
    ts
    thresh
    mask_extend
    debug

    Returns
    -------

    """
    median = np.median(ts)
    deviations = np.abs(ts-median)
    mad = np.median(deviations)
    mask = deviations > (mad*thresh)
    if debug:
        plt.plot(deviations)
        plt.plot(mask*deviations.max(),'o')
    new_mask = mask.copy()
    for offset in range(1,mask_extend):
        new_mask[:-offset] |= mask[offset:]
        new_mask[offset:] |= mask[:-offset]
    mask = new_mask
#    mask[:-mask_extend] = (~mask[:-mask_extend] | ~mask[mask_extend:])
#    mask[mask_extend:] = mask[mask_extend:] | mask[:-mask_extend]
    if debug:
        plt.plot(mask*deviations.max(),'x',mew=2)
    return mask


def deglitch_mask_mad(ts,thresh=5,mask_extend=50,window_length=2**8):
    full_mask = np.zeros(ts.shape,dtype='bool')
    step = window_length//2
    if step > ts.shape[0]:
        step = ts.shape[0]
    nstep = ts.shape[0]//step
    for k in xrange(nstep):
        start = k-1
        if start < 0:
            start = 0
        chunk = ts[start*step:(k+1)*step]
        mask = deglitch_mask_block_mad(chunk,thresh=thresh,mask_extend=mask_extend)
        full_mask[start*step:((start+1)*step)] |= mask[:step]
    full_mask[start*step:start*step+len(mask)] |= mask
    return full_mask

def mask_glitches(ts_list,mask,window_length):
    if type(ts_list) is np.ndarray:
        ts_list = [ts_list]
    step = window_length//2
    nstep = ts_list[0].shape[0]//step
    clean_ts = [ts.copy() for ts in ts_list]
    for k in xrange(nstep):
        start = k-1
        if start < 0:
            start = 0
        local_mask = mask[start*step:(k+1)*step]
        for clean in clean_ts:
            chunk = clean[start*step:(k+1)*step]
            nmask = local_mask.sum()
            if nmask:
                chunk[local_mask] = np.random.choice(chunk[~local_mask],nmask)
    return clean_ts

def deglitch_new(ts,thresh=6,mask_extend=50,window_length=2**16):
    clean,mask = deglitch_mask_mad(np.abs(ts),thresh=thresh,mask_extend=mask_extend,window_length=window_length)
    clean = ts.copy()
    clean[mask] = np.array(random.sample(ts[~mask],mask.sum()))
    return clean