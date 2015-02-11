#!/usr/bin/env python

# This is the code to run experiment 
# Please refer to --help for arguments setting
#
# before running the experiment, please make sure to execute 
# data_preprocessing.m and  transform_matdata2pydata.py to transformt the mat 
# format data into python .npz
#
# by Cameron Po-Hsuan Chen @ Princeton


import numpy as np, scipy, random, sys, math, os
import scipy.io
from scipy import stats
import random
import argparse
from scikits.learn.svm import NuSVC
#from alignment_algo import *
import importlib
#import sys


## argument parsing
usage = '%(prog)s dataset nvoxel nTR  exptype [--loo] [--expopt] [--winsize] \
align_algo [-k kernel] niter nfeature [-r RANDSEED]'
parser = argparse.ArgumentParser(usage=usage)

parser.add_argument("dataset",    help="name of the dataset")
parser.add_argument("nvoxel", type = int,
                    help="number of voxels in the dataset")
parser.add_argument("nTR", type = int,
                    help="number of TRs in the dataset")

parser.add_argument("exptype",    help="name of the experiment type")
parser.add_argument("-l", "--loo", action="store_true" , 
                    help="whether this experiment is loo experiment")
parser.add_argument("--expopt",    help="experiment options e.g. 1st or 2nd")
parser.add_argument("-w", "--winsize", type = int,
                    help="mysseg winsize")

parser.add_argument("align_algo", help="name of the alignment algorithm")
parser.add_argument("-k", "--kernel", metavar='',
                    help="type of kernel to use")

parser.add_argument("niter"     , type = int,  
                    help="number of iterations to the algorithm")
parser.add_argument("nfeature", type=int, 
                    help="number of features")
parser.add_argument("-r", "--randseed", type=int, metavar='',
                    help="random seed for initialization")

args = parser.parse_args()
print args

data_folder = args.dataset+'/'+str(args.nvoxel)+'vx/'+str(args.nTR)+'TR/'
exp_folder  = args.exptype + ("_loo" if args.loo else "" ) + \
              ("_"+args.expopt if args.expopt else "" ) + '/' 
alg_folder  = args.align_algo + ("_"+args.kernel if args.kernel else "") +'/'
opt_folder  = str(args.nfeature) + 'feat/' + \
              ("rand"+str(args.randseed)+'/' if args.randseed else "identity/" )

# rondo options
options = {'input_path'  : '/jukebox/ramadge/pohsuan/pHA/data_v2/input/'+data_folder,\
           'working_path': '/fastscratch/pohsuan/pHA/data_v2/working/'+\
                            data_folder+exp_folder+alg_folder+opt_folder,\
           'output_path' : '/jukebox/ramadge/pohsuan/pHA/data_v2/output/'+\
                            data_folder+exp_folder+alg_folder+opt_folder}

print options

# load data for alignment and prediction
# load movie data after voxel selection by matdata_preprocess.m 
if args.exptype == 'imgpred':
  movie_data_lh = scipy.io.loadmat(options['input_path']+'movie_data_lh.mat')
  movie_data_rh = scipy.io.loadmat(options['input_path']+'movie_data_rh.mat')
  align_data_lh = movie_data_lh['movie_data_lh'] 
  align_data_rh = movie_data_rh['movie_data_rh'] 
  
  mkdg_data_lh = scipy.io.loadmat(options['input_path']+'mkdg_data_lh.mat')
  mkdg_data_rh = scipy.io.loadmat(options['input_path']+'mkdg_data_rh.mat')
  pred_data_lh = mkdg_data_lh['mkdg_data_lh'] 
  pred_data_rh = mkdg_data_rh['mkdg_data_rh']
elif args.exptype == 'mysseg':
  if not args.winsize or not args.expopt:
    exist('mysseg experiment need arg winsize expopt')
  movie_data_lh = scipy.io.loadmat(options['input_path']+'movie_data_lh.mat')
  movie_data_rh = scipy.io.loadmat(options['input_path']+'movie_data_rh.mat')
  movie_data_lh = movie_data_lh['movie_data_lh'] 
  movie_data_rh = movie_data_rh['movie_data_rh'] 

  movie_data_lh_1st = movie_data_lh[:,0:nTR/2,:]
  movie_data_lh_2nd = movie_data_lh[:,(nTR/2+1):nTR,:]
  movie_data_rh_1st = movie_data_rh[:,0:nTR/2,:]
  movie_data_rh_2nd = movie_data_rh[:,(nTR/2+1):nTR,:]

  align_data_lh = np.zeros((movie_data_lh_1st.shape))
  align_data_rh = np.zeros((movie_data_rh_1st.shape))
  pred_data_lh  = np.zeros((movie_data_lh_2nd.shape))
  pred_data_rh  = np.zeros((movie_data_rh_2nd.shape))

  if '1st' == args.expopt:
    for m in range(nsubjs):
      align_data_lh[:,:,m] = stats.zscore(movie_data_lh_1st[:,:,m].T ,axis=0, ddof=1).T 
      align_data_rh[:,:,m] = stats.zscore(movie_data_rh_1st[:,:,m].T ,axis=0, ddof=1).T 
      pred_data_lh[:,:,m]  = stats.zscore(movie_data_lh_2nd[:,:,m].T ,axis=0, ddof=1).T 
      pred_data_rh[:,:,m]  = stats.zscore(movie_data_rh_2nd[:,:,m].T ,axis=0, ddof=1).T
  elif '2nd' == args.expopt:
    for m in range(nsubjs):
      align_data_lh[:,:,m] = stats.zscore(movie_data_lh_2nd[:,:,m].T ,axis=0, ddof=1).T 
      align_data_rh[:,:,m] = stats.zscore(movie_data_rh_2nd[:,:,m].T ,axis=0, ddof=1).T 
      pred_data_lh[:,:,m]  = stats.zscore(movie_data_lh_1st[:,:,m].T ,axis=0, ddof=1).T 
      pred_data_rh[:,:,m]  = stats.zscore(movie_data_rh_1st[:,:,m].T ,axis=0, ddof=1).T
  else:
    exit('missing 1st or 2nd arg for mysseg experiment')
else:
  exit('invalid experiment type')

(nvoxel_align, nTR_align, nsubjs_align) = align_data_lh.shape
(nvoxel_pred , nTR_pred , nsubjs_pred)  = pred_data_lh.shape

# make sure the dimension of dataset is consistent with input args
assert nvoxel_pred == nvoxel_align
assert nvoxel_pred == args.nvoxel
assert nsubjs_pred == nsubjs_align
nsubjs = nsubjs_pred 
assert nTR_align == args.nTR

# run alignment
algo = importlib.import_module('alignment_algo.'+args.align_algo)
for i in range(args.niter):
  new_niter_lh = algo.align(align_data_lh, options, args, 'lh')
  new_niter_rh = algo.align(align_data_rh, options, args, 'rh')

  # make sure right and left brain alignment are working at the same iterations
  assert new_niter_lh == new_niter_rh

  # load transformation matrices
  if args.align_algo != 'None' :
    workspace_lh = np.load(options['working_path']+para['align_algo']+'_lh_'+str(new_niter_lh)+'.npz')
    workspace_rh = np.load(options['working_path']+para['align_algo']+'_rh_'+str(new_niter_rh)+'.npz')

  # prepare training and testing data
  transform_lh = np.zeros((args.nvoxel,args.nfeature,nsubjs))
  transform_rh = np.zeros((args.nvoxel,args.nfeature,nsubjs))
 
  # load transformation matrices into transform for projecting testing data
  if args.align_algo in ['ha']:
    transform_lh = workspace_lh['R']
    transform_rh = workspace_rh['R']
  elif args.align_algo in ['pha_em','spha_vi']:
    bW_lh = workspace_lh['bW']
    bW_rh = workspace_rh['bW']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh[m*nvoxel:(m+1)*nvoxel,:]
      transform_rh[:,:,m] = bW_rh[m*nvoxel:(m+1)*nvoxel,:]
  elif args.align_algo in ['ppca','pica']:
    bW_lh = workspace_lh['R']
    bW_rh = workspace_rh['R']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh
      transform_rh[:,:,m] = bW_rh
  elif args.align_algo in ['ha_sm_retraction','ha_sm_newton']:
    bW_lh = workspace_lh['W']
    bW_rh = workspace_rh['W']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh[:,:,m]
      transform_rh[:,:,m] = bW_rh[:,:,m]
  elif args.align_algo == 'None' :
    for m in range(nsubjs):
      transform_lh[:,:,m] = np.identity(nvoxel)
      transform_rh[:,:,m] = np.identity(nvoxel)
  else :
    exit('alignment algo not recognize')


  # transformed mkdg data with learned transformation matrices
  transformed_data = np.zeros((args.nfeature*2 , nTR_pred ,nsubjs))

  for m in range(nsubjs):
    trfed_lh_tmp = transform_lh[:,:,m].T.dot(pred_data_lh[:,:,m])
    trfed_rh_tmp = transform_rh[:,:,m].T.dot(pred_data_rh[:,:,m])
    transformed_data[:,:,m] = stats.zscore( np.vstack((trfed_lh_tmp,trfed_rh_tmp)).T ,axis=0, ddof=1).T

  accu = np.zeros(shape=nsubjs)

  if args.exptype == 'imgpred':
    # image stimulus prediction 
    for tst_subj in range(nsubjs):
      tst_data = transformed_data[:,:,tst_subj]

      trn_subj = range(nsubjs)
      trn_subj.remove(tst_subj)

      for m in range(nsubjs-1):
        trn_data[:,m*56:(m+1)*56] = transformed_data[:,:,trn_subj[m]]

      # scikit-learn svm for classification
      clf = NuSVC(nu=0.5, kernel = 'linear')
      clf.fit(trn_data.T, trn_label)
      pred_label = clf.predict(tst_data.T)
      
      accu[loo] = sum(pred_label == tst_label)/float(len(pred_label))
  elif args.exptype == 'mysseg':
    winsize = args.winsize
    nseg = nTR_pred - win_size
    # mysseg prediction prediction
    trn_data = np.zeros((args.nfeature*2*win_size, nseg))

    # the trn data also include the tst data, but will be subtracted when 
    # calculating A
    for m in range(nsubjs):
      for w in range(win_size):
        trn_data[w*2*args.nfeature:(w+1)*2*args.nfeature,:] += transformed_data[:,w:(w+nseg),m]

    for tst_subj in range(nsubjs):
      tst_data = np.zeros((args.nfeature*2*win_size, nseg))
      for w in range(win_size):
        tst_data[w*2*args.nfeature:(w+1)*2*args.nfeature,:] = transformed_data[:,w:(w+nseg),tst_subj]
    
      A =  stats.zscore((trn_data - tst_data),axis=0, ddof=1)
      B =  stats.zscore(tst_data,axis=0, ddof=1)
      corr_mtx = B.T.dot(A)

      for i in range(nseg):
        for j in range(nseg):
          if abs(i-j)<win_size and i != j :
            corr_mtx[i,j] = -np.inf

      rank =  np.argmax(corr_mtx, axis=1)
      accu[loo] = sum(rank == range(nseg)) / float(nseg)

  np.savez_compressed(options['working_path']+'acc_'+str(new_niter_lh)+'.npz',accu = accu)
  print np.mean(accu) 
