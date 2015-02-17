#!/usr/bin/env python
import scipy.io
import os,sys
import numpy as np
import mvpa2
from mvpa2.datasets.mri import fmri_dataset
from scipy.signal import butter, lfilter


roi = 'pt'
template_path = '/jukebox/fastscratch/pohsuan/pHA/data/raw/forest/'+\
                'psydata.ovgu.de/forrest_gump/templates/grpbold7Tad/from_mni/'
mask_fname = os.path.join(template_path, roi+'_mask.nii.gz')
nsubj = 20
nrun  = 8
nTR_remove = 4

# Sample rate and desired cutoff frequencies (in Hz).
fs = 1/2.0 #one sample every two seconds
lowcut = 1/150.0
highcut = 1/9.0 

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

forrest_movie_all = np.empty((nsubj,1), dtype=object)

for i in range(nsubj):
  filename = '/jukebox/ramadge/pohsuan/pHA/data/raw/forrest_'+roi+'/forrest_movie_'+roi+str(i)+'.npz' 
  ws = np.load(filename)
  subj_data = ws['arr_0']
  forrest_movie_all[i,0] = subj_data[()]['subj_data']
scipy.io.savemat('/jukebox/ramadge/pohsuan/pHA/data/raw/forrest_'+roi+'/forrest_movie_'+roi+'_distributed.mat', {'forrest_movie_all': forrest_movie_all})



