
import scipy.io
import os,sys
import numpy as np
import mvpa2
from mvpa2.datasets.mri import fmri_dataset
from scipy.signal import butter, lfilter

roi = 'tom_noLR'
template_path = '/jukebox/ramadge/RAW_DATA/green_eye/masks/'
mask_fname = os.path.join(template_path, 'theory_mind_pFgA_z_FDR_0.01_reverse_3mm.nii.gz')
# mask_fname = os.path.join(template_path, 'auditory_cortex_mask_thr15.nii.gz')

group1 = range(1,15)+range(29,35)
group2 = range(15,28)+range(35,40)
group_all = group1+group2
start = [21, 20, 19, 20, 20, 16, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 19, 20, 20,
          20, 20, 20, 20, 19, 20, 20, 20, 20, 20, 20, 20, 20, 15, 20, 19, 20, 20, 20, 20]
end = [470, 469, 468, 469, 469, 465, 469, 469, 469, 469, 469, 469, 469, 469, 469, 469, 469, 468, 469, 469,
       469, 469, 469, 469, 468, 469, 469, 469, 469, 469, 469, 469, 469, 464, 469, 468, 469, 469, 469, 469]
nsubj = 40

greeneye_movie_all = np.empty((nsubj,1), dtype=object)
for subj in range(nsubj):

    datapath = '/jukebox/ramadge/RAW_DATA/green_eye/niftis/'

    # getting first run data
    bold_fname = os.path.join(datapath, 'subj{}_trans_filtered_func_data.nii'.format(subj+1))
    print bold_fname
    data_tmp = fmri_dataset(bold_fname,mask = mask_fname)
    subj_data = data_tmp.samples.T
    subj_data = subj_data[:, start[subj]:end[subj] ]
    greeneye_movie_all[subj,0] = subj_data
os.mkdir('/jukebox/ramadge/pohsuan/pHA/data/raw/greeneye_'+roi+'/')
scipy.io.savemat('/jukebox/ramadge/pohsuan/pHA/data/raw/greeneye_'+roi+'/greeneye_movie_'+roi+'.mat', {'movie_all': greeneye_movie_all})


