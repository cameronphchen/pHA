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

nfeature = [10,50,100,500,1000,1300]

acc_HA_all             = np.zeros((nsubjs, 1))
acc_HA_rand_all        = np.zeros((nsubjs*nrand, 1))
acc_pHA_EM_all         = np.zeros((nsubjs, 1))
acc_pHA_EM_lowrank_all = np.zeros((nsubjs*nrand, len(nfeature)))
acc_no_align           = np.zeros((nsubjs*nrand, 1))

#taking the ith iteration
i = 8

# HA 
ws_ha = np.load(options['working_path']+'acc_HA_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
acc_HA_all[0:nsubjs,0]        = ws_ha['accu']
ws_ha.close()

acc_HA_mean = acc_HA_all.mean(axis = 0).tolist()
acc_HA_se   = acc_HA_all.std(axis = 0)/math.sqrt(2*nsubjs)

# HA Random
for rand in range(nrand):
  ws_ha_rand = np.load(options['working_path']+'HA_rand/HA_rand_'+str(rand)+'/acc_HA_rand'+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
  acc_HA_rand_all[range(rand*nsubjs,(rand+1)*nsubjs),0]     = ws_ha_rand['accu']
  ws_ha_rand.close()

acc_HA_rand_mean = acc_HA_rand_all.mean(axis = 0).tolist()
acc_HA_rand_se   = acc_HA_rand_all.std(axis = 0)/math.sqrt(2*nsubjs)

#pHA_EM
ws_pha_em = np.load(options['working_path']+'acc_pHA_EM_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
acc_pHA_EM_all[0:nsubjs,0] = ws_pha_em['accu'] 
ws_pha_em.close()

acc_pHA_EM_mean = acc_pHA_EM_all.mean(axis = 0)
acc_pHA_EM_se   = acc_pHA_EM_all.std(axis = 0)/math.sqrt(2*nsubjs)

#pHA_EM_lowrank
for k in range(len(nfeature)):
  for rand in range(nrand):
    ws_pha_em_lowrank = np.load(options['working_path']+ 'lowrank'+str(nfeature[k]) +'/rand'+str(rand)+\
                                  '/acc_pHA_EM_lowrank_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    acc_pHA_EM_lowrank_all[range(rand*nsubjs,(rand+1)*nsubjs),k]     = ws_pha_em_lowrank['accu'] 
    ws_pha_em_lowrank.close()

acc_pHA_EM_lowrank_mean = acc_pHA_EM_lowrank_all.mean(axis = 0)
acc_pHA_EM_lowrank_se   = acc_pHA_EM_lowrank_all.std(axis = 0)/math.sqrt(nsubjs)

# no alignment
ws_none = np.load(options['working_path']+'acc_None_'+str(para['nvoxel'])+'vx_0.npz')
for rand in range(nrand):
  acc_no_align[range(rand*nsubjs,(rand+1)*nsubjs),0]     = ws_none['accu'] 

no_align_mean = acc_no_align.mean(axis = 0)
no_align_se   = acc_no_align.std(axis = 0)/math.sqrt(nsubjs)

# set font size
font = {'size'   : 5}

plt.rc('font', **font)

aspectratio=6

# plot accuracy
#acc_HA_all             = np.zeros((nsubjs*2, 1))
#acc_HA_rand_all        = np.zeros((nsubjs*2*nrand, 1))
#acc_pHA_EM_all         = np.zeros((nsubjs*2, 1))
#acc_pHA_EM_lowrank_all = np.zeros((2*nsubjs*nrand, len(nfeature)))
#acc_no_align           = np.zeros((2*nsubjs*nrand, 1))
#                     0          1          2          3         4        5         6         7          8          9         10           11            
name = np.array(('No\nAlignment','HA\nIdentity','HA\nRandom','pHA\nIdentity','pHA 10\nRandom','pHA 50\nRandom','pHA 100\nRandom',
                  'pHA 500\nRandom','pHA 1000\nRandom','pHA 1300\nRandom','Neuron HA','Neuron\nAnatomical', 'Within\nSubject'))
idx = range(len(name))

all_mean = np.zeros((len(name)))
all_mean[0] = no_align_mean[0]
all_mean[1] = acc_HA_mean[0] 
all_mean[2] = acc_HA_rand_mean[0]
all_mean[3] = acc_pHA_EM_mean[0]
all_mean[4] = acc_pHA_EM_lowrank_mean[0]
all_mean[5] = acc_pHA_EM_lowrank_mean[1]
all_mean[6] = acc_pHA_EM_lowrank_mean[2]
all_mean[7] = acc_pHA_EM_lowrank_mean[3]
all_mean[8] = acc_pHA_EM_lowrank_mean[4]
all_mean[9] = acc_pHA_EM_lowrank_mean[5] 
all_mean[10] = 0.639
all_mean[11]=  0.446 
all_mean[12]=  0.632 

all_se   = np.zeros((len(name)))
all_se[0] = no_align_se[0]
all_se[1] = acc_HA_se [0]
all_se[2] = acc_HA_rand_se[0] 
all_se[3] = acc_pHA_EM_se[0]
all_se[4] = acc_pHA_EM_lowrank_se[0]
all_se[5] = acc_pHA_EM_lowrank_se[1]
all_se[6] = acc_pHA_EM_lowrank_se[2]
all_se[7] = acc_pHA_EM_lowrank_se[3]
all_se[8] = acc_pHA_EM_lowrank_se[4]
all_se[9] = acc_pHA_EM_lowrank_se[5] 
all_se[10]= 0.022
all_se[11]= 0.014
all_se[12]= 0.021

  
plt.figure()
bar_width= 0.1
opacity = 0.4
error_config = {'ecolor': '0'}
rects = plt.bar(idx, all_mean,yerr=all_se, align='center', color='b', alpha=opacity, error_kw=error_config)
plt.xticks(idx, name)
plt.ylabel('Accuracy')
plt.xlabel('Alignment Methods')
plt.ylim([0,0.8])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
plt.title('Image Classification')

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.axes().text(rect.get_x()+rect.get_width()/2., height+0.03, '%.3f'%float(height),
                ha='center', va='bottom')

autolabel(rects)

plt.savefig(options['output_path']+'BAR_accuracy_lowrank_rand_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')



