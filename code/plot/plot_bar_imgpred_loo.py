#!/usr/bin/env python
# plot barchart for image prediction across different algorithms  
import pprint
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math
import pickle
import os

parser = argparse.ArgumentParser()
parser.add_argument("dataset",    help="name of the dataset")
parser.add_argument("nvoxel", 
                    help="number of voxels in the dataset")
parser.add_argument("nTR", 
                    help="number of TRs in the dataset")
parser.add_argument("nsubjs"     , type = int,  
                    help="number of subjects in the dataset")
parser.add_argument("niter"     ,   
                    help="number of iterations to the algorithm")
parser.add_argument("nrand"     , type = int,  
                    help="number of random initilization to average")

args = parser.parse_args()
print '--------------experiment arguments--------------'
pprint.pprint(args.__dict__,width=1)

#####################List out all the algos to show in fig#####################

os.system("python create_algo_list.py")
pkl_file = open('algo_list.pkl', 'rb')
algo_list = pickle.load(pkl_file)
pkl_file.close()

###############################################################################

name = []
for algo in algo_list:
  name.append(algo['name'])

all_mean = np.zeros((len(name)))
all_se   = np.zeros((len(name)))

data_folder = args.dataset+'/'+args.nvoxel+'vx/'+args.nTR+'TR/'
exp_folder  = 'imgpred/' 

working_path = '/fastscratch/pohsuan/pHA/data/working/'+data_folder+exp_folder
output_path  = '/jukebox/ramadge/pohsuan/pHA/data/output/'

for i, algo in enumerate(algo_list):
  algo_folder  = algo['align_algo'] + ("_"+algo['kernel'] if algo['kernel'] else "") +'/'
  filename    = algo['align_algo']+'_acc_'+args.niter +'.npz'

  if algo['rand'] == False:
    acc_tmp=[]
    for loo in xrange(args.nsubjs):
      opt_folder  = algo['nfeature']+'feat/identity/loo'+str(loo)+'/'
      ws = np.load(working_path + algo_folder + opt_folder + filename) 
      acc_tmp.append(ws['accu'])
      ws.close()
    all_mean[i] = np.mean(acc_tmp)
    all_se  [i] = np.std(acc_tmp)/math.sqrt(args.nsubjs) 
  else:
    acc_tmp = []
    for rnd in xrange(args.nrand):
      for loo in xrange(args.nsubjs):
        opt_folder  = algo['nfeature']+'feat/'+'rand'+str(rnd)+'/loo'+str(loo)+'/'
        ws = np.load(working_path + algo_folder + opt_folder + filename) 
        acc_tmp.append(ws['accu'])
        ws.close()
    all_mean[i] = np.mean(acc_tmp)
    all_se  [i] = np.std(acc_tmp)/math.sqrt(args.nsubjs)

# set font size
font = {'family' : 'serif',
        'size'   : 12}

plt.rc('text', usetex=True)
plt.rc('font', **font)

all_mean = np.insert(all_mean,1,0.632)
all_se = np.insert(all_se,1,0.021)
name.insert(1,'Within Subject')

aspectratio=4
idx = range(len(name))

plt.figure()
error_config = {'ecolor': '0'}
rects = plt.bar(idx, all_mean, yerr=all_se, align='center', error_kw=error_config)
rects[1].set_color('c')
rects[4].set_color('r')
plt.xticks(idx, name,rotation='vertical')
plt.ylabel('Accuracy')
#plt.xlabel('Alignment Methods')
plt.xlim([-1,8])
plt.ylim([0,0.8])
plt.axes().set_aspect(aspectratio)
plt.legend(loc=4)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.axes().text(rect.get_x()+rect.get_width()/2., height+0.03, '%.3f'%float(height),
                ha='center', va='bottom')

autolabel(rects)
#plt.text(.12, .05, 'Image Category Prediction', horizontalalignment='right', verticalalignment='top')
plt.title('Image Stimulus Prediction LOO {} {}vx {}TRs'.format(args.dataset.replace('_','-'),args.nvoxel, args.nTR))
filename_list = ['bar_accuracy', args.dataset , args.nvoxel+'vx', args.nTR+'TR' ,\
                'imgpred_loo_'+ args.niter+'thIter']
plt.savefig(output_path + '_'.join(filename_list) + '.eps', format='eps', dpi=200,bbox_inches='tight')
