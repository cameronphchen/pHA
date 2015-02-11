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
usage = '%(prog)s dataset nvoxel nTR  exptype [--loo] [--expopt] align_algo [-k kernel] \
 niter nfeature [-r RANDSEED]'
parser = argparse.ArgumentParser(usage=usage)

parser.add_argument("dataset",    help="name of the dataset")
parser.add_argument("nvoxel",     help="number of voxels in the dataset")
parser.add_argument("nTR",        help="number of TRs in the dataset")

parser.add_argument("exptype",    help="name of the experiment type")
parser.add_argument("-l", "--loo", action="store_true" , 
                    help="whether this experiment is loo experiment")
parser.add_argument("--expopt",    help="experiment options")

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

data_folder = args.dataset+'/'+args.nvoxel+'vx/'+args.nTR+'TR/'
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

# load data for alignment
# load movie data after voxel selection by matdata_preprocess.m 
movie_data_lh = scipy.io.loadmat(options['input_path']+'movie_data_lh.mat')
movie_data_rh = scipy.io.loadmat(options['input_path']+'movie_data_rh.mat')
align_data_lh = movie_data_lh['movie_data_lh'] 
align_data_rh = movie_data_rh['movie_data_rh'] 


algo = importlib.import_module('alignment_algo.'+args.align_algo)
for i in range(args.niter):
  new_niter_lh = algo.align(align_data_lh, options, args, 'lh')
  new_niter_rh = algo.align(align_data_rh, options, args, 'rh')
