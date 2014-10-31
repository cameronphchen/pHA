pHA
===

location: '/Volumes/ramadge/pohsuan/pHA'
Test
1. First ordered list item
2. Another item
⋅⋅* Unordered sub-list. 
1. Actual numbers don't matter, just that it's a number
⋅⋅1. Ordered sub-list
4. And another item.

⋅⋅⋅You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown).

⋅⋅⋅To have a line break without a paragraph, you will need to use two trailing spaces.⋅⋅
⋅⋅⋅Note that this line is separate, but within the same paragraph.⋅⋅
⋅⋅⋅(This is contrary to the typical GFM line break behaviour, where trailing spaces are not required.)

* Unordered list can use asterisks
- Or minuses
+ Or pluses


======================
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

Experiment code:

  1.run_exp.py
    -align on whole movie, test on image

  2.run_exp_img_align.py
    -align on image test on image

  3.run_exp_img_align_loo.py
    -align on image with leave-one-out framework 

  4.run_exp_loo.py
    -align on whole movie, test on image, loo

  5.run_exp_mysseg.py
    -align on half movie, myster segment identification on another half movie

  6.run_exp_mysseg_img_align.py
    -align on image and myster segment on half movie

  7.run_exp_mysseg_loo.py
    -align on half movie, myster segment identification on another half movie
    -with loo framework

Run experiment in batch script:

  1.SH_run_exp_loo_rand.sh

  2.SH_run_exp_mysseg_loo_rand.sh

  3.SH_run_exp_mysseg_lowrank_rand.sh

  4.SH_run_exp_mysseg_rand.sh

  5.SH_run_exp_rand.sh

  6.SH_run_exp_rand_lowrank.sh


Algorithm code:

  1.ha.py
    - standard implemntation of hyperalignment
    - identity initialization for transformation matrix

  2.ha_rand.py
    - standard implemntation of hyperalignment
    - random orthogonal initialization for transformation matrix    
    - random orthogonal is calculated with QR decomposition of 
      nvoxel by nvoxel random matrix

  3.ha_swaroop.py
    - hyperalignment with hack that's try to be as similar as 
      "HPAL/code/compute_transformations" but in python

  4.pha_em.py
    - constrained EM algorithm for probabilistic hyperalignment
    - identity initialization for transformation matrix

  5.pha_em_lowrank.py
    - constrained EM algorithm for probabilistic hyperalignment
    - random skinny matrix with orthonormal columns initialization 
      for transformation matrix
    - random skinny matrix is calculated with QR decomposition of 
      nvoxel by nfeature random matrix    

  6.pha_em_rand.py
    - constrained EM algorithm for probabilistic hyperalignment
    - random orthogonal is calculated with QR decomposition of 
      nvoxel by nvoxel random matrix

Plot code:

  1.plot_accuracy.py

  2.plot_accuracy_loo.py

  3.plot_accuracy_loo_rand.py

  4.plot_accuracy_lowrank_rand.py

  5.plot_accuracy_mysseg.py

  6.plot_accuracy_mysseg_RHA.py

  7.plot_accuracy_mysseg_loo.py

  8.plot_accuracy_mysseg_loo_rand.py

  9.plot_accuracy_mysseg_lowrank_rand.py

  10.plot_accuracy_mysseg_rand.py

  11.plot_accuracy_rand.py

  12.plot_loglikelihood.py

  13.plot_noiselevel.py


=====================================
May 17, 2014
  1. Print out the result of sigma for pHA_EM, the number is weird. First, some times it shows up as negative number
     , later iterations, the number becomes way too large, up to 1e+159. There must be a bug within the code
     or within the equations

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

