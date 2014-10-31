#!/usr/bin/env python

# this is the code that runs the whole type 1 experiment
# for type 2 experiment, please refer to run_exp_loo.py
# 
# this code run a specific alignment algorithm (align_algo) for (niter) rounds
# with voxel selection algorithm selecting (nvoxel) amount of voxels
# and (nTR) TR of movie data for alignment 
# using both right and left VT data
#
# before running the experiment, please make sure to execute data_preprocessing.m and  transform_matdata2pydata.py to transformt the mat format data into python .npz
#
# align_algo = 'HA', 'HA_shuffle', 'pHA_EM', 'pHA_EM_shuffle', 'None'
# 
# example: run_exp.py (align_algo) (n_iter) (n_voxel) (n_TR)
#          run_exp.p  HA  100  1300  2201
#
# by Cameron Po-Hsuan Chen @ Princeton


import numpy as np, scipy, random, sys, math, os
import scipy.io
from scipy import stats
import random
from libsvm.svmutil import *
from scikits.learn.svm import NuSVC
from ha import HA
from ha_swaroop import HA_swaroop
from pha_em import pHA_EM
import sys
sys.path.append('/Users/ChimatChen/anaconda/python.app/Contents/lib/python2.7/site-packages/')


# load experiment parameters
para  = {'align_algo': sys.argv[1],\
         'niter'     : int(sys.argv[2]),\
         'nvoxel'    : int(sys.argv[3]),\
         'nTR'       : int(sys.argv[4]),\
         'nsubjs'    : 10,\
         'niter_unit': 1 }

print para

niter      = para['niter']
nvoxel     = para['nvoxel']
nTR        = para['nTR']
nsubjs     = para['nsubjs']
niter_unit = para['niter_unit']
win_size   = 6 #TR
# load experiment options
# rondo options
options = {'input_path'  : '/jukebox/ramadge/pohsuan/pHA/data/input/', \
           'working_path': '/mnt/cd/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
           'output_path' : '/jukebox/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

# local options
#options = {'input_path'  : '/Volumes/ramadge/pohsuan/pHA/data/input/', \
#           'working_path': '/Volumes/ramadge/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
#           'output_path' : '/Volumes/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

# load movie data after voxel selection by matdata_preprocess.m 
movie_data_lh = scipy.io.loadmat(options['working_path']+'movie_data_lh_'+str(para['nvoxel'])+'vx.mat')
movie_data_rh = scipy.io.loadmat(options['working_path']+'movie_data_rh_'+str(para['nvoxel'])+'vx.mat')
movie_data_lh = movie_data_lh['movie_data_lh'] 
movie_data_rh = movie_data_rh['movie_data_rh'] 

movie_data_lh_1st = movie_data_lh[:,0:nTR/2,:]
movie_data_lh_2nd = movie_data_lh[:,(nTR/2+1):nTR,:]
movie_data_rh_1st = movie_data_rh[:,0:nTR/2,:]
movie_data_rh_2nd = movie_data_rh[:,(nTR/2+1):nTR,:]

######################################### used for image classification, should be deleted
mkdg_data_lh = scipy.io.loadmat(options['working_path']+'mkdg_data_lh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_rh = scipy.io.loadmat(options['working_path']+'mkdg_data_rh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_lh = mkdg_data_lh['mkdg_data_lh'] 
mkdg_data_rh = mkdg_data_rh['mkdg_data_rh']

# load label for testing data
label = scipy.io.loadmat(options['input_path']+'subjall_picall_label.mat')
label = label['label']
trn_label = label[0:504]
tst_label = label[504:560]
trn_label = np.squeeze(np.asarray(trn_label))
tst_label = np.squeeze(np.asarray(tst_label))
#########################################

if 'shuffle' in para['align_algo'] :
  print 'shuffle'
  time_idx = range(0,nTR/2)
  random.seed(0)
  time_idx = random.sample(time_idx,nTR/2)
  if '1st' in para['align_algo']: 
    movie_data_lh_1st = movie_data_lh_1st[:,time_idx,:]
    movie_data_rh_1st = movie_data_rh_1st[:,time_idx,:]
  elif '2nd' in para['align_algo']: 
    movie_data_lh_2nd = movie_data_lh_2nd[:,time_idx,:]
    movie_data_rh_2nd = movie_data_rh_2nd[:,time_idx,:]

movie_data_lh_trn = np.zeros((movie_data_lh_1st.shape))
movie_data_rh_trn = np.zeros((movie_data_rh_1st.shape))
movie_data_lh_tst = np.zeros((movie_data_lh_2nd.shape))
movie_data_rh_tst = np.zeros((movie_data_rh_2nd.shape))

if '1st' in para['align_algo']:
  for m in range(nsubjs):
    movie_data_lh_trn[:,:,m] = stats.zscore(movie_data_lh_1st[:,:,m].T ,axis=0, ddof=1).T
    movie_data_lh_tst[:,:,m] = stats.zscore(movie_data_lh_2nd[:,:,m].T ,axis=0, ddof=1).T 
    movie_data_rh_trn[:,:,m] = stats.zscore(movie_data_rh_1st[:,:,m].T ,axis=0, ddof=1).T 
    movie_data_rh_tst[:,:,m] = stats.zscore(movie_data_rh_2nd[:,:,m].T ,axis=0, ddof=1).T 
elif '2nd' in para['align_algo']:
  for m in range(nsubjs):
    movie_data_lh_trn[:,:,m] = stats.zscore(movie_data_lh_2nd[:,:,m].T ,axis=0, ddof=1).T 
    movie_data_lh_tst[:,:,m] = stats.zscore(movie_data_lh_1st[:,:,m].T ,axis=0, ddof=1).T 
    movie_data_rh_trn[:,:,m] = stats.zscore(movie_data_rh_2nd[:,:,m].T ,axis=0, ddof=1).T 
    movie_data_rh_tst[:,:,m] = stats.zscore(movie_data_rh_1st[:,:,m].T ,axis=0, ddof=1).T 

# for niter/niter_unit round, each round the alignment algorithm will run niter_unit iterations
for i in range(para['niter']/para['niter_unit']):
  # alignment phase
  # fit the model to movie data with number of iterations
  if  'HA_mysseg' in para['align_algo'] or 'HA_shuffle_mysseg' in  para['align_algo'] :
    new_niter_lh = HA(movie_data_lh_trn, options, para, 'lh')
    new_niter_rh = HA(movie_data_rh_trn, options, para, 'rh')
  elif 'pHA_EM_mysseg' in para['align_algo'] or 'pHA_EM_shuffle_mysseg' in  para['align_algo'] :
    new_niter_lh = pHA_EM(movie_data_lh_trn, options, para, 'lh')
    new_niter_rh = pHA_EM(movie_data_rh_trn, options, para, 'rh')
  elif para['align_algo'] == 'None' :
    # without any alignment, set new_niter_lh and new_niter_rh=0, the corresponding transformation
    # matrices are identity matrices
    new_niter_lh = new_niter_rh = 0
  else :
    print 'alignment algo not recognize'

  print 'align done',
  #make sure right and left brain alignment are working at the same iterations
  assert new_niter_lh == new_niter_rh

  # load transformation matrices
  if not para['align_algo'] == 'None':
    workspace_lh = np.load(options['working_path']+para['align_algo']+'_lh_'+str(para['nvoxel'])+'vx_'+str(new_niter_lh)+'.npz')
    workspace_rh = np.load(options['working_path']+para['align_algo']+'_rh_'+str(para['nvoxel'])+'vx_'+str(new_niter_rh)+'.npz')

  if 'HA_mysseg' in para['align_algo'] or 'HA_shuffle_mysseg' in  para['align_algo'] :
    transform_lh = workspace_lh['R']
    transform_rh = workspace_rh['R']
  elif 'pHA_EM_mysseg' in para['align_algo'] or 'pHA_EM_shuffle_mysseg' in  para['align_algo'] :
    transform_lh = np.zeros((nvoxel,nvoxel,nsubjs))
    transform_rh = np.zeros((nvoxel,nvoxel,nsubjs))
    bW_lh = workspace_lh['bW']
    bW_rh = workspace_rh['bW']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh[m*nvoxel:(m+1)*nvoxel,:]
      transform_rh[:,:,m] = bW_rh[m*nvoxel:(m+1)*nvoxel,:]
  elif para['align_algo'] == 'None' :
    transform_lh = np.zeros((nvoxel,nvoxel,nsubjs))
    transform_rh = np.zeros((nvoxel,nvoxel,nsubjs))
    for m in range(nsubjs):
      transform_lh[:,:,m] = np.identity(nvoxel)
      transform_rh[:,:,m] = np.identity(nvoxel)
  else :
    print 'alignment algo not recognize'

######################################### used for image classification, should be deleted
#
#  # classification
#  transformed_data = np.zeros((para['nvoxel']*2 ,56 ,para['nsubjs']))
#
#  # transformed mkdg data with learned transformation matrices
#  for m in range(para['nsubjs']):
#    trfed_lh_tmp = transform_lh[:,:,m].T.dot(mkdg_data_lh[:,:,m])
#    trfed_rh_tmp = transform_rh[:,:,m].T.dot(mkdg_data_rh[:,:,m])
#    transformed_data[:,:,m] = stats.zscore( np.vstack((trfed_lh_tmp,trfed_rh_tmp)).T ,axis=0, ddof=1).T
#
#  tst_data = np.zeros(shape = (para['nvoxel']*2,56))
#  trn_data = np.zeros(shape = (para['nvoxel']*2,504))
#  accu = np.zeros(shape=10)
#
#  for loo in range(para['nsubjs']):
#      tst_data = transformed_data[:,:,loo]
#
#      loo_idx = range(para['nsubjs'])
#      loo_idx.remove(loo)
#
#      for m in range(para['nsubjs']-1):
#        trn_data[:,m*56:(m+1)*56] = transformed_data[:,:,loo_idx[m]]
#
#      # scikit-learn svm for classification
#      clf = NuSVC(nu=0.5, kernel = 'linear')
#      clf.fit(trn_data.T, trn_label)
#      pred_label = clf.predict(tst_data.T)
#      
#      accu[loo] = sum(pred_label == tst_label)/float(len(pred_label))
#
#  print accu
#
##################################################################

  print 'load tranf matrix',
  sys.stdout.flush()
  movie_data_tst = np.zeros((nvoxel*2,nTR/2,nsubjs))
  movie_data_tst_tmp = np.zeros((nvoxel*2))
  for t in range(nTR/2):
    if (t % 100) == 0:
      print '.',
      sys.stdout.flush()
    for m in range(nsubjs):
      movie_data_tst_tmp[0:nvoxel]        = transform_lh[:,:,m].T.dot(movie_data_lh_tst[:,t,m])
      movie_data_tst_tmp[nvoxel:2*nvoxel] = transform_rh[:,:,m].T.dot(movie_data_rh_tst[:,t,m])
      movie_data_tst[:,t,m] = movie_data_tst_tmp/np.linalg.norm(movie_data_tst_tmp)
  

  accu = np.zeros(nsubjs)
  for loo in range(nsubjs):
    print '-',
    subj_idx = range(nsubjs)
    subj_idx.remove(loo)
    mean_response = movie_data_tst[:,:,subj_idx].mean(axis = 2)
    loo_response  = movie_data_tst[:,:,loo]
    assert mean_response.shape[0] == nvoxel*2
    assert mean_response.shape[1] == nTR/2
   
    corr_mtx_tmp = mean_response.T.dot(loo_response)
    corr_mtx = np.zeros((nTR/2-win_size,nTR/2-win_size))
    for i in range(corr_mtx.shape[0]):
      for j in range(corr_mtx.shape[1]):
        for v in range(win_size):
          corr_mtx[i,j] += corr_mtx_tmp[i+v,j+v] 

    for i in range(corr_mtx.shape[0]):
      for v in range(1,win_size):
        if (i+v) < corr_mtx.shape[0]:
          corr_mtx[i+v,i] = -np.inf
        if (i-v) >= 0:
          corr_mtx[i-v,i] = -np.inf

    rank =  np.argmax(corr_mtx, axis=0) 
    accu[loo] = sum(rank == range(nTR/2-win_size)) / float(nTR/2-win_size)

  print accu  
  np.savez_compressed(options['working_path']+'acc_'+para['align_algo']+'_'+str(para['nvoxel'])+'vx_'+str(new_niter_lh)+'.npz',accu = accu)



################################ hao's implementation
  print 'load tranf matrix',
  sys.stdout.flush()
  movie_data_tst_tmp = np.zeros((nvoxel*2,nTR/2,nsubjs))
  for t in range(nTR/2):
    if (t % 100) == 0:
      print '.',
      sys.stdout.flush()
    for m in range(nsubjs):
      movie_data_tst_tmp[0:nvoxel,t,m]        = transform_lh[:,:,m].T.dot(movie_data_lh_tst[:,t,m])
      movie_data_tst_tmp[nvoxel:2*nvoxel,t,m] = transform_rh[:,:,m].T.dot(movie_data_rh_tst[:,t,m])

   
  movie_data

  accu = np.zeros(nsubjs)
  for loo in range(nsubjs):
    print '-',
    subj_idx = range(nsubjs)
    subj_idx.remove(loo)
    mean_response = movie_data_tst[:,:,subj_idx].mean(axis = 2)
    loo_response  = movie_data_tst[:,:,loo]
    assert mean_response.shape[0] == nvoxel*2
    assert mean_response.shape[1] == nTR/2
   
    corr_mtx_tmp = mean_response.T.dot(loo_response)
    corr_mtx = np.zeros((nTR/2-win_size,nTR/2-win_size))
    for i in range(corr_mtx.shape[0]):
      for j in range(corr_mtx.shape[1]):
        for v in range(win_size):
          corr_mtx[i,j] += corr_mtx_tmp[i+v,j+v] 

    for i in range(corr_mtx.shape[0]):
      for v in range(1,win_size):
        if (i+v) < corr_mtx.shape[0]:
          corr_mtx[i+v,i] = -np.inf
        if (i-v) >= 0:
          corr_mtx[i-v,i] = -np.inf

    rank =  np.argmax(corr_mtx, axis=0) 
    accu[loo] = sum(rank == range(nTR/2-win_size)) / float(nTR/2-win_size)

  print accu  
  np.savez_compressed(options['working_path']+'acc_'+para['align_algo']+'_'+str(para['nvoxel'])+'vx_'+str(new_niter_lh)+'.npz',accu = accu)



