#!usr/bin/env python


# matdata2pydata.py (nvoxel) (nTR)

import numpy as np, scipy, random, sys, math, os
import scipy.io

nvoxel    = int(sys.argv[1])
nTR       = int(sys.argv[2])
nsubjs    = 10

working_path = '/fastscratch/pohsuan/pHA/data/working/'+str(nTR)+'TR/'

movie_data_lh = scipy.io.loadmat(working_path+'movie_data_lh_'+str(nvoxel)+'vx.mat')
movie_data_rh = scipy.io.loadmat(working_path+'movie_data_rh_'+str(nvoxel)+'vx.mat')
movie_data_lh = movie_data_lh['movie_data_lh'] 
movie_data_rh = movie_data_rh['movie_data_rh'] 

mkdg_data_lh = scipy.io.loadmat(working_path+'mkdg_data_lh_'+str(nvoxel)+'vx.mat')
mkdg_data_rh = scipy.io.loadmat(working_path+'mkdg_data_rh_'+str(nvoxel)+'vx.mat')
mkdg_data_lh = mkdg_data_lh['mkdg_data_lh'] 
mkdg_data_rh = mkdg_data_rh['mkdg_data_rh']

np.savez_compressed(working_path+'movie_data_lh_'+str(nvoxel)+'vx.npz', movie_data_lh = movie_data_lh);
np.savez_compressed(working_path+'movie_data_rh_'+str(nvoxel)+'vx.npz', movie_data_rh = movie_data_rh);
np.savez_compressed(working_path+'mkdg_data_lh_'+str(nvoxel)+'vx.npz', mkdg_data_lh = mkdg_data_lh);
np.savez_compressed(working_path+'mkdg_data_rh_'+str(nvoxel)+'vx.npz', mkdg_data_rh = mkdg_data_rh);
