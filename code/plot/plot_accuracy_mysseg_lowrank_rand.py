#!/usr/bin/env python

# by Cameron Po-Hsuan Chen @ Princeton

import numpy as np, scipy, random, sys, math, os
import scipy.io
from scipy import stats

sys.path.append('/Users/ChimatChen/anaconda/python.app/Contents/lib/python2.7/site-packages/')

from libsvm.svmutil import *
from scikits.learn.svm import NuSVC

import numpy as np
import matplotlib.pyplot as plt
import sys

# load experiment parameters
para  = {'niter'     : int(sys.argv[1]),\
         'nvoxel'    : int(sys.argv[2]),\
         'nTR'       : int(sys.argv[3]),\
         'nrand'     : int(sys.argv[4]),\
         'nsubjs'    : 10,\
         'niter_unit': 1 }

niter      = para['niter']
nvoxel     = para['nvoxel']
nTR        = para['nTR']
nsubjs     = para['nsubjs']
niter_unit = para['niter_unit']
nrand      = para['nrand']

# load experiment options
# rondo options
options = {'input_path'  : '/jukebox/ramadge/pohsuan/pHA/data/input/', \
           'working_path': '/fastscratch/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
           'output_path' : '/jukebox/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

# local options
#options = {'input_path'  : '/Volumes/ramadge/pohsuan/pHA/data/input/', \
#           'working_path': '/Volumes/ramadge/pohsuan/pHA/data/working/'+str(para['nTR'])+'TR/',\
#           'output_path' : '/Volumes/ramadge/pohsuan/pHA/data/output/'+str(para['nTR'])+'TR/'}

nfeature = [50,100,500,1000,1300]

acc_pHA_EM_lowrank_all = np.zeros((2*nsubjs*nrand, niter/niter_unit, len(nfeature)))
acc_pHA_EM_all = np.zeros((nsubjs, niter/niter_unit))

for i in range(1,niter/niter_unit):
  ws_pha_em = np.load(options['working_path']+'acc_pHA_EM_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
  acc_pHA_EM_all[:,i] = ws_pha_em['accu']
  ws_pha_em.close()
  for k in range(len(nfeature)):
    for rand in range(nrand):
      ws_pha_em_lowrank_mysseg_1st = np.load(options['working_path']+ 'lowrank'+str(nfeature[k]) +'/rand'+str(rand)+'/pHA_EM_lowrank_mysseg_1st'+\
                                  '/acc_pHA_EM_lowrank_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
      ws_pha_em_lowrank_mysseg_2nd = np.load(options['working_path']+ 'lowrank'+str(nfeature[k]) +'/rand'+str(rand)+'/pHA_EM_lowrank_mysseg_2nd'+\
                                  '/acc_pHA_EM_lowrank_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
      acc_pHA_EM_lowrank_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),i,k]     = ws_pha_em_lowrank_mysseg_1st['accu'] 
      acc_pHA_EM_lowrank_all[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),i,k] = ws_pha_em_lowrank_mysseg_2nd['accu'] 
      ws_pha_em_lowrank_mysseg_1st.close()
      ws_pha_em_lowrank_mysseg_2nd.close()

ws_none = np.load(options['working_path']+'acc_None_'+str(para['nvoxel'])+'vx_0.npz')
acc_None_mean = ws_none['accu'].mean(axis = 0)
acc_None_se   = ws_none['accu'].std(axis = 0)/math.sqrt(nsubjs)

iter_range = range(niter/niter_unit)

acc_pHA_EM_mean = acc_pHA_EM_all.mean(axis = 0)
acc_pHA_EM_se   = acc_pHA_EM_all.std(axis = 0)/math.sqrt(nsubjs)
acc_pHA_EM_mean[0] = acc_None_mean
acc_pHA_EM_se[0]   = acc_None_se

# set font size
font = {#'family' : 'normal',
        'size'   : 15}

plt.rc('font', **font)

aspectratio=8

# plot accuracy
plt.figure()
#sys.exit()

color_code = 'cbgkmy'

plt.errorbar(iter_range ,acc_pHA_EM_mean,acc_pHA_EM_se  , label='pHA EM orig' , linewidth=2, color='r')
for k in range(len(nfeature)):
  acc_pHA_EM_lowrank_mean = acc_pHA_EM_lowrank_all[:,:,k].mean(axis = 0)
  acc_pHA_EM_lowrank_se   = acc_pHA_EM_lowrank_all[:,:,k].std(axis = 0)/math.sqrt(nsubjs)
  acc_pHA_EM_lowrank_mean[0] = acc_None_mean
  acc_pHA_EM_lowrank_se[0]   = acc_None_se
  plt.errorbar(iter_range ,acc_pHA_EM_lowrank_mean,acc_pHA_EM_lowrank_se  , label='pHA EM '+str(nfeature[k]) , linewidth=2, color=color_code[k])
plt.xlabel('Iterations')
plt.ylabel('Accuracy')
plt.ylim([0,0.8])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
plt.savefig(options['output_path']+'accuracy_mysseg_lowrank_rand_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')

