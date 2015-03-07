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
image_fname     = 'attention_brain_N12_GAM_REML_mni.hdf5.gz'
mask_fname      = 'vt_masks_unique_N19_FS_mni.hdf5.gz'

#ds_mask_origin  = h5load(template_path+mask_fname)
ds_image        = h5load(template_path+image_fname)

movie_order = ['er00', 'zi00', 'ok00', 'sn00', 'as00',
               'pc01', 'kw00', 'ad01', 'ks00', 'hm00', 
               'pa00', 'ap01', 'ab00', 'kr00', 'pk00', 
               'jg00', 'ls00', 'lr00', 'mg00']
image_order = ['kr00', 'jg00', 'pa00', 'ap01', 'hm00', 
               'ks00', 'lr00', 'er00', 'zi00', 'kw00',
               'sn00', 'as00']

condition_list = [
'bird eating',
'bird fighting',
'bird running',
'bird swimming',
'bug eating',
'bug fighting',
'bug running',
'bug swimming',
'primate eating',
'primate fighting',
'primate running',
'primate swimming',
'ungulate eating',
'ungulate fighting',        
'ungulate running',
'ungulate swimming',
'reptile swimming',
'reptile running',
'reptile fighting',
'reptile eating']

animal_list = ['bird','bug','primate','ungulate','reptile']
action_list = ['eating','fighting','running','swimming']
task_list   = ['action','animal']

condition_label = []
animal_label    = []
action_label    = []
task_label      = []

for l in ds_image[0].sa['conditions'].value:
    condition_label.append(condition_list.index(l))

for l in ds_image[0].sa['animals'].value:
    animal_label.append(animal_list.index(l))

for l in ds_image[0].sa['actions'].value:
    action_label.append(action_list.index(l))

for l in ds_image[0].sa['task'].value:
    task_label.append(task_list.index(l))

f = open('/jukebox/ramadge/pohsuan/pHA/data/raw/nature_'+roi+'/condition_label.txt', 'w')
for l in condition_label:
    f.write('{}'.format(l))

f = open('/jukebox/ramadge/pohsuan/pHA/data/raw/nature_'+roi+'/animal_label.txt', 'w')
for l in animal_label:
    f.write('{}'.format(l))

f = open('/jukebox/ramadge/pohsuan/pHA/data/raw/nature_'+roi+'/action_label.txt', 'w')
for l in action_label:
    f.write('{}'.format(l))

f = open('/jukebox/ramadge/pohsuan/pHA/data/raw/nature_'+roi+'/task_label.txt', 'w')
for l in task_label:
    f.write('{}'.format(l))

