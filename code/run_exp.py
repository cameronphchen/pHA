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
# align_algo = 'HA', 'pHA', 'None'
# 
# example: run_exp.py (align_algo) (n_iter) (n_voxel) (n_TR)
#          run_exp.p  HA  100  1300  2201
#
# by Cameron Po-Hsuan Chen @ Princeton


import numpy as np, scipy, random, sys, math, os
import scipy.io
from scipy import stats


from libsvm.svm import *
from libsvm.svmutil import *
from scikits.learn.svm import NuSVC
from ha import HA
from ha_swaroop import HA_swaroop

import sys

def trace(frame, event, arg):
    print "%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno)
    return trace


os.remove('ha.pyc')

# load experiment parameters
para  = {'align_algo': sys.argv[1],\
         'niter'     : int(sys.argv[2]),\
         'nvoxel'    : int(sys.argv[3]),\
         'nTR'       : int(sys.argv[4]),\
         'nsubjs'    : 10,\
         'niter_unit': 1 }


# load experiment options
# rondo options
options = {'input_path'  : '/mnt/cd/ramadge/pohsuan/pHA/data/input/', \
           'working_path': '/mnt/cd/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
           'output_path' : '/mnt/cd/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

# local options
#options = {'input_path'  : '/Volumes/ramadge/pohsuan/pHA/data/input/', \
#           'working_path': '/Volumes/ramadge/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
#           'output_path' : '/Volumes/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}



# load raw data
movie_data_lh = scipy.io.loadmat(options['working_path']+'movie_data_lh_'+str(para['nvoxel'])+'vx.mat')
movie_data_rh = scipy.io.loadmat(options['working_path']+'movie_data_rh_'+str(para['nvoxel'])+'vx.mat')
movie_data_lh = movie_data_lh['movie_data_lh'] 
movie_data_rh = movie_data_rh['movie_data_rh'] 

mkdg_data_lh = scipy.io.loadmat(options['working_path']+'mkdg_data_lh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_rh = scipy.io.loadmat(options['working_path']+'mkdg_data_rh_'+str(para['nvoxel'])+'vx.mat')
mkdg_data_lh = mkdg_data_lh['mkdg_data_lh'] 
mkdg_data_rh = mkdg_data_rh['mkdg_data_rh']

label = scipy.io.loadmat(options['input_path']+'subjall_picall_label.mat')
label = label['label']
trn_label = label[0:504]
tst_label = label[504:560]
trn_label = np.squeeze(np.asarray(trn_label))
tst_label = np.squeeze(np.asarray(tst_label))

for i in range(para['niter']/para['niter_unit']):
  
  # alignment phase
  # fit the model to movie data with number of iterations

  new_niter_lh = HA(movie_data_lh, options, para, 'lh')
  new_niter_rh = HA(movie_data_rh, options, para, 'rh')
#  new_niter_lh = HA_swaroop(movie_data_lh, options, para, 'lh')
#  new_niter_rh = HA_swaroop(movie_data_rh, options, para, 'rh')
#  new_niter_lh = new_niter_rh = 0
  assert new_niter_lh == new_niter_rh


  # classfication
  workspace_lh = np.load(options['working_path']+'HA_lh_'+str(para['nvoxel'])+'vx_'+str(new_niter_lh)+'.npz')
  workspace_rh = np.load(options['working_path']+'HA_rh_'+str(para['nvoxel'])+'vx_'+str(new_niter_rh)+'.npz')
  transform_lh = workspace_lh['R']
  transform_rh = workspace_rh['R']


  transformed_data = np.zeros((para['nvoxel']*2 ,56 ,para['nsubjs']))
  for m in range(para['nsubjs']):
    # with alignment
    trfed_lh_tmp = transform_lh[:,:,m].T.dot(mkdg_data_lh[:,:,m])
    trfed_rh_tmp = transform_rh[:,:,m].T.dot(mkdg_data_rh[:,:,m])
    # without alignment
#    trfed_lh_tmp = mkdg_data_lh[:,:,m]
#    trfed_rh_tmp = mkdg_data_rh[:,:,m]

    transformed_data[:,:,m] = stats.zscore( np.vstack((trfed_lh_tmp,trfed_rh_tmp)).T ,axis=0, ddof=1).T


  tst_data = np.zeros(shape = (para['nvoxel']*2,56))
  trn_data = np.zeros(shape = (para['nvoxel']*2,504))

  accu = np.zeros(shape=10)

  for loo in range(para['nsubjs']):
      tst_data = transformed_data[:,:,loo]

      loo_idx = range(para['nsubjs'])
      loo_idx.remove(loo)

      for m in range(para['nsubjs']-1):
        trn_data[:,m*56:(m+1)*56] = transformed_data[:,:,loo_idx[m]]

      # scikit-lean
      clf = NuSVC(nu=0.5, kernel = 'linear')
      clf.fit(trn_data.T, trn_label)
      pred_label = clf.predict(tst_data.T)
      
      # libsvm
      #trn_label_list = trn_label.tolist()
      #tst_label_list = tst_label.tolist()
      #trn_data_T_tolist = trn_data.T.tolist()
      #tst_data_T_tolist = tst_data.T.tolist()
      #prob = svm_problem(trn_label_list,trn_data_T_tolist)
      #param = svm_parameter('-s 1 -t 0 -n 0.5 -p 0.001')
      #m = svm_train(prob, param)
      #svm_predict(tst_label_list,tst_data_T_tolist,m)    

      accu[loo] = sum(pred_label == tst_label)/float(len(pred_label))

  np.savez_compressed(options['working_path']+'acc_HA_'+str(para['nvoxel'])+'vx_'+str(new_niter_lh)+'.npz',accu = accu)
  print np.mean(accu) 



