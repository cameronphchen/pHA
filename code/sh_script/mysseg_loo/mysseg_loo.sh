#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [-l, --loo] [-e, --expopt] [-w, --winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

#raider, forrest_pt, nature_vt
#1300  , 1300      , 850
#2203  , 3535      , 1509

#dataset='raider'
#nvoxel=1300
#nTR=2203
#niter=10

submittype='submit'
dataset='raider'
nvoxel=1300
nTR=2203
niter=1
winsize=9
nsubj=9

ln -s /jukebox/ramadge/pohsuan/pHA/code/run_exp.py run_exp.py
chmod +x run_exp.py
for loo in  $(seq 0 $nsubj)
do

    #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize noalign $niter $nvoxel --strfresh
    #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize noalign $niter $nvoxel --strfresh
    #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize ha      $niter $nvoxel --strfresh
    #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize ha      $niter $nvoxel --strfresh
    for nfeat in 10  50 100 500 1300
    do 
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize ppca   $niter $nfeat --strfresh
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize ppca   $niter $nfeat --strfresh 
        for rand in   $(seq 0 4)
        do
            #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize pha_em  $niter $nfeat -r $rand --strfresh
            #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize pha_em  $niter $nfeat -r $rand --strfresh
            #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize spha_vi $niter $nfeat -r $rand --strfresh
            #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize spha_vi $niter $nfeat -r $rand --strfresh
            #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize pica    $niter $nfeat -r $rand --strfresh
            #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize pica    $niter $nfeat -r $rand --strfresh
            #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize ha_syn  $niter $nfeat -r $rand --strfresh
            #$submittype run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize ha_syn  $niter $nfeat -r $rand --strfresh
        done
    done
done
