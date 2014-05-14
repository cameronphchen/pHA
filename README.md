pHA
===

location: '/Volumes/ramadge/pohsuan/pHA'

Goal: 

1. write cleaner code that replicate swaroop's result in python
  2. try to use as few hack as possible
  3. figure out what's the effect of swaroop's hack in terms of accuracy and time
  4. easy incorporation of future algorithms, especially the extension of probabilistic HA

Structure:

  1. matdata_preprocess.m : 
     process the whole data received from swaroop with exactly the same data 
     preprocessing and store in python friendly format

  2. run_exp.py :
     (1) import data from output of matdata_preprocess.m 
     (2) conduct alignment, depends on the specifiy alignment algorithm
     (3) conduct type 1 experiment (as MLSP paper)
     (4) allow checking prediction accuracy every niter_unit iteration
     (5) run niter iteration and stop
     (6) able to select number of TR and number of voxel 
     (7) the number of TR and voxel need to be identical to the input paramter
         of matdata_preprocess.m

  3. ha.py :
     standard implementation of hyperalignment, without any hack

  4. ha_swaroop.py:
     hyperalignment with hack that's try to be as similar as 
     "HPAL/code/compute_transformations" but in python

=====================================

May 13, 2014
  1. Reach benchmark performance 64% (align with Neuron result) with HA with both VT 1300 vx, 2203 TRs

May 11, 2014

  1. Basic framework finished

  2. The data processing file "matdata_preprocess.m" will process data the same way as swaroop's HPAL

  3. without doing alignment, the data feed into classifier NuSVC is identical 
     to HPAL

  3.1 Be careful of python stats.zscore, the dim argument is working weird, currently
     try to manually feed in transposed data 

  3.2 Be careful of python svd, the output is U s V, where A = U * np.diag(s) * V
     V is the V^T that we used to use

  4. [TODO] the classification result w/o alignment is different from HPAL w/o
     alignment, seems to be the problem of Scikit-lean. Different by 1%, but should
     be identical.
     - ask pni-help to update scikit-learn in rondo, current 0.8, latest stable 0.14
     - verbose=true in NuSVC initialization (not available in v0.8, but in v0.14)
     - http://stackoverflow.com/questions/15254243/different-accuracy-for-libsvm-and-scikit-learn
     - study Cython, see how NuSVC use libsvm different from the way we used to use

  5. [TODO] classification with hyperalignment is very different from the result of 
     HPAL (2203TR, 1300vx). differ by around 5%. 
     - HPAL ~64%
     - ha_swaroop works better ~59%
     - ha ~55%

  6. [TODO] write unit test for making sure the data preprocessing is correct, by 
     comaring the result of processed data to a stored sample data from HAPL

  7. [TODO] think about how to write the structure so that it can incorporate 
     more future stuff

