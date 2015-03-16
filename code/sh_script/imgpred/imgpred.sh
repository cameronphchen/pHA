#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [--loo] [--expopt] [--winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

#raider, forrest_pt, nature_vt
#1300  , 1300      , 850
#2203  , 3535      , 1509

#dataset='raider'
#nvoxel=1300
#nTR=2203
#niter=10

dataset='nature_vt'
nvoxel=850
nTR=1509
niter=1

ln -s /jukebox/ramadge/pohsuan/pHA/code/run_exp.py run_exp.py
chmod +x run_exp.py
#submit_long run_exp.py $dataset $nvoxel $nTR imgpred noalign $niter $nvoxel --strfresh
submit run_exp.py $dataset $nvoxel $nTR imgpred ha      $niter $nvoxel --strfresh
#submit_long run_exp.py $dataset $nvoxel $nTR imgpred ha_syn  $niter $nvoxel --strfresh
for nfeat in 10 50 100 400 500 600 700 850  #10 50 100 500 1300 #10 50 100 400 500 600 700 850 
do
  #submit_long run_exp.py $dataset $nvoxel 2203 imgpred ppca 10 $nfeat --strfresh
  for rand in $(seq 0 4)
  do
    #submit      run_exp.py $dataset $nvoxel $nTR imgpred pica   $niter $nfeat -r $rand --strfresh
    submit run_exp.py $dataset $nvoxel $nTR imgpred ha_syn $niter $nfeat -r $rand --strfresh
    #submit_long run_exp.py $dataset $nvoxel $nTR imgpred pha_em $niter $nfeat -r $rand --strfresh
    #submit_long run_exp.py $dataset $nvoxel $nTR imgpred spha_vi $niter $nfeat -r $rand --strfresh
    #submit_long run_exp.py $dataset $nvoxel $nTR imgpred ha_sm_retraction $niter $nfeat -r $rand --strfresh
  done
done
