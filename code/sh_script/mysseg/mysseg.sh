#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [-l, --loo] [-e, --expopt] [-w, --winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

## experiment configuration

#raider, forrest_pt, nature_vt
#1300  , 1300      , 850
#2203  , 3535      , 1509

# raider, forrest_pt: 10 50 100 500 1300
# nature_vt: 10 50 100 400 500 600 700 850


submittype='submit'
dataset='raider'
nvoxel=1300
nTR=2203       
winsize=9
niter=1

ln -s /jukebox/ramadge/pohsuan/pHA/code/run_exp.py run_exp.py
chmod +x run_exp.py
#$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize noalign $niter $nvoxel --strfresh
#$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize noalign $niter $nvoxel --strfresh
#$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize ha      $niter $nvoxel --strfresh
#$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize ha      $niter $nvoxel --strfresh
for nfeat in 10 50 100 500 1300
do
    $submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize ppca   $niter $nfeat --strfresh
    $submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize ppca   $niter $nfeat --strfresh
    for rand in $(seq 0 4)
    do
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize pha_em  $niter $nfeat -r $rand --strfresh
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize pha_em  $niter $nfeat -r $rand --strfresh
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize spha_vi $niter $nfeat -r $rand --strfresh
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize spha_vi $niter $nfeat -r $rand --strfresh
        $submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize pica    $niter $nfeat -r $rand --strfresh
        $submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize pica    $niter $nfeat -r $rand --strfresh
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize ha_syn  $niter $nfeat -r $rand --strfresh
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize ha_syn  $niter $nfeat -r $rand --strfresh
    done
done
