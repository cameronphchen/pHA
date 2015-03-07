#!/usr/bin/env python

import scipy.io
import os,sys
import numpy as np
import sys
sys.path.insert(0,'/jukebox/ramadge/pohsuan/PyMVPA-hyper')
import mvpa2
from mvpa2.base.hdf5 import h5load

roi = 'vt'
template_path   = '/jukebox/ramadge/RAW_DATA/nature_movie_animal_action/'
movie_fname     = 'life_movie_brain_N19_blur4.0_dil3_mni.hdf5.gz'
image_fname     = 'attention_brain_N12_GAM_REML_mni.hdf5.gz'
mask_fname      = 'vt_masks_unique_N19_FS_mni.hdf5.gz'

ds_movie_origin = h5load(template_path+movie_fname)
ds_mask_origin  = h5load(template_path+mask_fname)
ds_image        = h5load(template_path+image_fname)

movie_order = ['er00', 'zi00', 'ok00', 'sn00', 'as00',
               'pc01', 'kw00', 'ad01', 'ks00', 'hm00', 
               'pa00', 'ap01', 'ab00', 'kr00', 'pk00', 
               'jg00', 'ls00', 'lr00', 'mg00']
image_order = ['kr00', 'jg00', 'pa00', 'ap01', 'hm00', 
               'ks00', 'lr00', 'er00', 'zi00', 'kw00',
               'sn00', 'as00']

ds_movie = []
ds_mask  = []
for subj in image_order:
    idx = movie_order.index(subj)
    ds_movie.append(ds_movie_origin[idx])
    ds_mask.append(ds_mask_origin[idx])

print 'start masking'
movie_all = np.empty((len(ds_movie),1), dtype=object)
image_all = np.empty((len(ds_image),1), dtype=object) 
for subj, (movie, image, mask) in enumerate(zip(ds_movie, ds_image, ds_mask)):
    idx       = np.where(mask.samples>0)
    subj_movie = movie.samples[:,idx[1]] 
    movie_all[subj,0] = subj_movie.T
    subj_image = image.samples[:,idx[1]]
    image_all[subj,0] = subj_image.T 


scipy.io.savemat('/jukebox/ramadge/pohsuan/pHA/data/raw/nature_'\
                 +roi+'/nature_movie_'+roi+'.mat', {'movie_all': movie_all})
scipy.io.savemat('/jukebox/ramadge/pohsuan/pHA/data/raw/nature_'\
                 +roi+'/nature_image_'+roi+'.mat', {'image_all': image_all})
print 'data saved'

