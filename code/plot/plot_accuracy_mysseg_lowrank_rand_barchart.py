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

acc_HA_all             = np.zeros((nsubjs*2, 1))
acc_HA_rand_all        = np.zeros((nsubjs*2*nrand, 1))
acc_pHA_EM_all         = np.zeros((nsubjs*2, 1))
acc_pHA_EM_lowrank_all = np.zeros((2*nsubjs*nrand, len(nfeature)))
acc_no_align           = np.zeros((2*nsubjs*nrand, 1))

#taking the ith iteration
i = 8

# HA 
ws_ha_mysseg_1st = np.load(options['working_path']+'acc_HA_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
ws_ha_mysseg_2nd = np.load(options['working_path']+'acc_HA_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
acc_HA_all[0:nsubjs,0]        = ws_ha_mysseg_1st['accu']
acc_HA_all[nsubjs:2*nsubjs,0] = ws_ha_mysseg_2nd['accu']
ws_ha_mysseg_1st.close()
ws_ha_mysseg_2nd.close()

acc_HA_mean = acc_HA_all.mean(axis = 0).tolist()
acc_HA_se   = acc_HA_all.std(axis = 0)/math.sqrt(2*nsubjs)

# HA Random
for rand in range(nrand):
  ws_ha_rand_mysseg_1st = np.load(options['working_path']+'rand'+str(rand)+'/HA_rand_mysseg_1st/'+'acc_HA_rand_mysseg_1st'+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
  ws_ha_rand_mysseg_2nd = np.load(options['working_path']+'rand'+str(rand)+'/HA_rand_mysseg_2nd/'+'acc_HA_rand_mysseg_2nd'+'_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
  acc_HA_rand_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),0]     = ws_ha_rand_mysseg_1st['accu']
  acc_HA_rand_all[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),0] = ws_ha_rand_mysseg_2nd['accu']
  ws_ha_rand_mysseg_1st.close()
  ws_ha_rand_mysseg_2nd.close()

acc_HA_rand_mean = acc_HA_rand_all.mean(axis = 0).tolist()
acc_HA_rand_se   = acc_HA_rand_all.std(axis = 0)/math.sqrt(2*nsubjs)

#pHA_EM
ws_pha_em_mysseg_1st = np.load(options['working_path']+'acc_pHA_EM_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
ws_pha_em_mysseg_2nd = np.load(options['working_path']+'acc_pHA_EM_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
acc_pHA_EM_all[0:nsubjs,0]        = ws_pha_em_mysseg_1st['accu'] 
acc_pHA_EM_all[nsubjs:2*nsubjs,0] = ws_pha_em_mysseg_2nd['accu'] 
ws_pha_em_mysseg_1st.close()
ws_pha_em_mysseg_2nd.close()

acc_pHA_EM_mean = acc_pHA_EM_all.mean(axis = 0)
acc_pHA_EM_se   = acc_pHA_EM_all.std(axis = 0)/math.sqrt(2*nsubjs)

#pHA_EM_lowrank
for k in range(len(nfeature)):
  for rand in range(nrand):
    ws_pha_em_lowrank_mysseg_1st = np.load(options['working_path']+ 'lowrank'+str(nfeature[k]) +'/rand'+str(rand)+'/pHA_EM_lowrank_mysseg_1st'+\
                                  '/acc_pHA_EM_lowrank_mysseg_1st_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    ws_pha_em_lowrank_mysseg_2nd = np.load(options['working_path']+ 'lowrank'+str(nfeature[k]) +'/rand'+str(rand)+'/pHA_EM_lowrank_mysseg_2nd'+\
                                  '/acc_pHA_EM_lowrank_mysseg_2nd_'+str(para['nvoxel'])+'vx_'+str(i)+'.npz')
    acc_pHA_EM_lowrank_all[range(2*rand*nsubjs,(2*rand+1)*nsubjs),k]     = ws_pha_em_lowrank_mysseg_1st['accu'] 
    acc_pHA_EM_lowrank_all[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),k] = ws_pha_em_lowrank_mysseg_2nd['accu'] 
    ws_pha_em_lowrank_mysseg_1st.close()
    ws_pha_em_lowrank_mysseg_2nd.close()

acc_pHA_EM_lowrank_mean = acc_pHA_EM_lowrank_all.mean(axis = 0)
acc_pHA_EM_lowrank_se   = acc_pHA_EM_lowrank_all.std(axis = 0)/math.sqrt(nsubjs)

# no alignment
ws_none_mysseg_1st = np.load(options['working_path']+'acc_None_mysseg_1st_'+str(para['nvoxel'])+'vx_0.npz')
ws_none_mysseg_2nd = np.load(options['working_path']+'acc_None_mysseg_2nd_'+str(para['nvoxel'])+'vx_0.npz')
for rand in range(nrand):
  acc_no_align[range(2*rand*nsubjs,(2*rand+1)*nsubjs),0]     = ws_none_mysseg_1st['accu'] 
  acc_no_align[range((2*rand+1)*nsubjs,2*(rand+1)*nsubjs),0] = ws_none_mysseg_2nd['accu']

no_align_mean = acc_no_align.mean(axis = 0)
no_align_se   = acc_no_align.std(axis = 0)/math.sqrt(nsubjs)

# plot accuracy
#acc_HA_all             = np.zeros((nsubjs*2, 1))
#acc_HA_rand_all        = np.zeros((nsubjs*2*nrand, 1))
#acc_pHA_EM_all         = np.zeros((nsubjs*2, 1))
#acc_pHA_EM_lowrank_all = np.zeros((2*nsubjs*nrand, len(nfeature)))
#acc_no_align           = np.zeros((2*nsubjs*nrand, 1))
#                     0          1          2          3         4        5         6         7          8          9         10           11            
#name = np.array(('No\nAlignment','HA\nIdentity','HA\nRandom','pHA\nIdentity','pHA 10\nRandom','pHA 50\nRandom','pHA 100\nRandom',
#                  'pHA 500\nRandom','pHA 1000\nRandom','pHA 1300\nRandom','Neuron HA','Neuron\nAnatomical'))
# name = np.array(('pHA$_{v0}$\nf=10','pHA$_{v0}$\nf=50','pHA$_{v0}$\nf=100','pHA$_{v0}$\nf=500','Haxby, 2011\n(HA)','Haxby, 2011\n(anatomical)'))
name = np.array(('pHA\nf=10','pHA\nf=50','pHA\nf=100','pHA\nf=500','Haxby, 2011\n(HA)','Haxby, 2011\n(anatomical)'))
idx = range(len(name))

all_mean = np.zeros(len(name))
all_se = np.zeros(len(name))


all_mean[0] = acc_pHA_EM_lowrank_mean[0]
all_mean[1] = acc_pHA_EM_lowrank_mean[1]
all_mean[2] = acc_pHA_EM_lowrank_mean[2]
all_mean[3] = acc_pHA_EM_lowrank_mean[3]
all_mean[4] = 0.706
all_mean[5]=  0.32 

all_se[0] = acc_pHA_EM_lowrank_se[0]
all_se[1] = acc_pHA_EM_lowrank_se[1]
all_se[2] = acc_pHA_EM_lowrank_se[2]
all_se[3] = acc_pHA_EM_lowrank_se[3]
all_se[4] = 0.026
all_se[5]=  0.025

#all_mean = np.zeros((len(name)))
#all_mean[0] = no_align_mean[0]
#all_mean[1] = acc_HA_mean[0] 
#all_mean[2] = acc_HA_rand_mean[0]
#all_mean[3] = acc_pHA_EM_mean[0]
#all_mean[4] = acc_pHA_EM_lowrank_mean[0]
#all_mean[5] = acc_pHA_EM_lowrank_mean[1]
#all_mean[6] = acc_pHA_EM_lowrank_mean[2]
#all_mean[7] = acc_pHA_EM_lowrank_mean[3]
#all_mean[8] = acc_pHA_EM_lowrank_mean[4]
#all_mean[9] = acc_pHA_EM_lowrank_mean[5] 
#all_mean[10] = 0.706
#all_mean[11]=  0.32 


#all_se   = np.zeros((len(name)))
#all_se[0] = no_align_se[0]
#all_se[1] = acc_HA_se [0]
#all_se[2] = acc_HA_rand_se[0] 
#all_se[3] = acc_pHA_EM_se[0]
#all_se[4] = acc_pHA_EM_lowrank_se[0]
#all_se[5] = acc_pHA_EM_lowrank_se[1]
#all_se[6] = acc_pHA_EM_lowrank_se[2]
#all_se[7] = acc_pHA_EM_lowrank_se[3]
#all_se[8] = acc_pHA_EM_lowrank_se[4]
#all_se[9] = acc_pHA_EM_lowrank_se[5] 
#all_se[10]= 0.026
#all_se[11]= 0.025

# set font size
font = {'family' : 'serif',
        'size'   : 10}

plt.rc('text', usetex=True)
plt.rc('font', **font)

aspectratio=6

plt.figure()
#opacity = 0
error_config = {'ecolor': '0'}
#rects = plt.bar(idx, all_mean,yerr=all_se, align='center', alpha=opacity, error_kw=error_config)
rects = plt.bar(idx, all_mean, yerr=all_se, align='center', error_kw=error_config)
rects[0].set_color('b')
rects[1].set_color('r')
rects[2].set_color('b')
rects[3].set_color('b')
rects[4].set_color('c')
rects[5].set_color('c')
plt.xticks(idx, name)
plt.ylabel('Accuracy')
#plt.xlabel('Alignment Methods')
plt.xlim([-0.6,5.6])
plt.ylim([0,1])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)
#plt.text(1.5, 0.93, 'Movie Segment Identification', horizontalalignment='left', verticalalignment='bottom')
plt.title('Movie Segment Identification')

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.axes().text(rect.get_x()+rect.get_width()/2., height+0.03, '%.3f'%float(height),
                ha='center', va='bottom')

autolabel(rects)
#plt.text(.12, .05, 'Movie Segment Classification', horizontalalignment='left', verticalalignment='bottom')
#plt.text(.12, .01, 'Skinny Random Matrices', horizontalalignment='left', verticalalignment='bottom')
plt.savefig(options['output_path']+'BAR_accuracy_mysseg_lowrank_rand_'+str(para['nvoxel'])+'vx.eps', format='eps', dpi=1000,bbox_inches='tight')


