
import scipy.io
import os,sys
import numpy as np
import mvpa2
from mvpa2.datasets.mri import fmri_dataset

template_path = '/jukebox/fastscratch/pohsuan/pHA/data/raw/forest/'+\
                'psydata.ovgu.de/forrest_gump/templates/grpbold7Tad/from_mni/'
act_mask_fname = os.path.join(template_path, 'act_mask.nii.gz')
nsubj = 19
nrun  = 8
forrest_movie_all = np.empty((nsubj,1), dtype=object)
for subj in range(nsubj):
    print subj,
    sys.stdout.flush()

    datapath = '/jukebox/fastscratch/pohsuan/pHA/data/raw/forest/'+\
               'psydata.ovgu.de/forrest_gump/sub0'+"%.2d" % (subj+1) +\
               '/BOLD/'

    # getting first run data
    run = 1
    runpath  = 'task001_run00'+str(run)+'/'
    bold_fname = os.path.join(datapath+runpath, 'bold_dico_dico7Tad2grpbold7Tad.nii.gz')
    data_tmp   = fmri_dataset(bold_fname,mask = act_mask_fname)
    subj_data  = data_tmp.samples.T
    # stack the rest to first run data
    for run in range(2,nrun+1):
        runpath  = 'task001_run00'+str(run)+'/'
        bold_fname = os.path.join(datapath+runpath, 'bold_dico_dico7Tad2grpbold7Tad.nii.gz')
        data_tmp   = fmri_dataset(bold_fname,mask = act_mask_fname)
        subj_data = np.hstack((subj_data,data_tmp.samples.T))

    forrest_movie_all[subj,0] = subj_data
scipy.io.savemat('/jukebox/ramadge/pohsuan/pHA/data/raw/forrest/forrest_movie_act.mat', {'forrest_movie_all': forrest_movie_all})
