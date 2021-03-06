#!/usr/bin/env python

# using pPCA for multisubject fMRI data alignment

#movie_data is a three dimensional matrix of size voxel x TR x nsubjs
#movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
#mathematic notation

# do PCA on bX (nvoxel x nsubjs*nTR)


import numpy as np, scipy, random, sys, math, os
from scipy import stats
import sys
sys.path.append('/jukebox/ramadge/pohsuan/scikit-learn/sklearn')
from sklearn.decomposition import PCA

def align(movie_data, options, args, lrh):
  print 'pPCA(scikit-learn)'
  nvoxel = movie_data.shape[0]
  nTR    = movie_data.shape[1]
  nsubjs = movie_data.shape[2]

  align_algo = args.align_algo
  nfeature   = args.nfeature
  
  if not os.path.exists(options['working_path']):
    os.makedirs(options['working_path'])

  # zscore the data
  bX = np.zeros((nsubjs*nTR,nvoxel))
  for m in range(nsubjs):
    for t in range(nTR):
      bX[nTR*m+t,:] = stats.zscore(movie_data[:,t,m].T ,axis=0, ddof=1)
  del movie_data

  U, s, VT = np.linalg.svd(bX, full_matrices=False)
  V = VT.T

  R = V[:,range(nfeature)]
  niter = 10 
  # initialization when first time run the algorithm
  np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(niter)+'.npz',\
                                R = R,  niter=niter)
  return niter
