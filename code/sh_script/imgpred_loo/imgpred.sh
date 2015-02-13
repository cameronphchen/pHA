#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [--loo] [--expopt] [--winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

ln -s /jukebox/ramadge/pohsuan/pHA/code/run_exp.py run_exp.py
chmod +x run_exp.py
for loo in $(seq 0 9)
do
  submit_long run_exp.py raider 1300 2203 imgpred --loo $loo ha 10 1300 --strfresh
  for nfeat in 10  50 100 500 1300
  do
    for rand in $(seq 0 4)
    do
      submit_long run_exp.py raider 1300 2203 imgpred --loo $loo pha_em 10 $nfeat -r $rand --strfresh
    done
  done
done
