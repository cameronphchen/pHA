#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [-l, --loo] [-e, --expopt] [-w, --winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

## experiment configuration

#raider, forrest_pt, nature_vt
#1300  , 1300      , 850
#2203  , 3535      , 1509

submittype='submit_long'
dataset='nature_vt' 
nvoxel=850      
nTR=1509         
winsize=9
niter=10

ln -s /jukebox/ramadge/pohsuan/pHA/code/run_exp.py run_exp.py
chmod +x run_exp.py
#$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize noalign $niter $nvoxel --strfresh
#$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize noalign $niter $nvoxel --strfresh
#$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize ha $niter $nvoxel --strfresh
#$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize ha $niter $nvoxel --strfresh
for nfeat in 10 50 100 400 500 600 700 850
do
    #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize pha_em $niter $nfeat --strfresh
    #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize pha_em $niter $nfeat --strfresh
    #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize ppca $niter $nfeat --strfresh
    #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize ppca $niter $nfeat --strfresh
    for rand in $(seq 0 4)
    do
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize pha_em $niter $nfeat -r $rand --strfresh
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize pha_em $niter $nfeat -r $rand --strfresh
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize pica $niter $nfeat -r $rand --strfresh
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize pica $niter $nfeat -r $rand --strfresh
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 1st -w $winsize ha_syn $niter $nfeat -r $rand --strfresh
        #$submittype run_exp.py $dataset $nvoxel $nTR mysseg -e 2nd -w $winsize ha_syn $niter $nfeat -r $rand --strfresh
    done
done
