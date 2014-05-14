#!/usr/bin/env python

# Standard Hyperalignment

# movie_data is a three dimensional matrix of size voxel x TR x nsubjs
# movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
# mathematic notation

import numpy as np, scipy, random, sys, math, os



def HA(movie_data, options, para):

  current_file = options['working_path']+'HA_'+str(para['nvoxel'])+'vx_current.npz' 

  if not os.path.exists(current_file): 
    R = np.zeros((para['nvoxel'],para['nvoxel'],para['nsubjs']))
    G = np.zeros((para['nTR'],para['nvoxel']))
    for m in range(nsubjs):
      R[:,:,m] = np.identity(para['nvoxel'])
      G = G + movie_data[:,:,m].T

  else:
    workspace = np.load(current_file)
    niter = workspace['niter']

    workspace = np.load(options['working_path']+'HA_'+str(para['nvoxel'])+'vx_'+str(niter)+'.npz')
    R = workspace['R'] 
    G = workspace['G']
    niter = workspace['niter']

  for i in range(0,para['niter_unit']):
    for m in range(nsubjs):
      G_tmp = G - movie[:,:,m].T.dot(R[:,:,m]) # G_tmp = G-XR
      U, s, V = np.linalg.svd(movie_data[:,:,m].dot(G), full_matrices=False) #USV^T = svd(X^TG)
      R[:,:,m] = U.dot(V.T) # R = UV^T
      G = G_tmp + movie[:,:,m].T.dot(R[:,:,m]) #G = G_tmp + XR


  np.savez_compressed(current_file, niter = niter+para['niter_unit'])
  np.savez_compressed(options['working_path']+'HA_'+str(para['nvoxel'])+'vx_'+str(niter+para['niter_unit'])+'.npz',\
                      R = R, G = G, niter=niter+para['niter_unit'])
  
  return
