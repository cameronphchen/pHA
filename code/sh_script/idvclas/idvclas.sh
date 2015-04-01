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

#run run_exp_noLR_idvclas.py greeneye_tom_noLR_thr15 5000 449 idvclas_svm --loo 1 ha_syn 10 50 -r 0 --strfresh

submittype='submit_long'
dataset='greeneye_tom_noLR_thr15'
exptype='idvclas_svm'
nvoxel=5000
nTR=449
niter=10
nsubj=19

ln -s /jukebox/ramadge/pohsuan/pHA/code/run_exp_noLR_idvclas.py run_exp_noLR_idvclas.py
chmod +x run_exp_noLR_idvclas.py
for nfeat_all in 0 #5 10 25 50 100
do
    for nfeat_group in 1000 #50 100 500 1000
    do
        for loo in $(seq 0 $nsubj)
        do
            #$submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo ppca $niter $nfeat --strfresh
            for rand in $(seq 0 4)
            do
                $submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo ha_syn $niter $nfeat_all $nfeat_group -r $rand --strfresh
                #$submittype run_exp_noLR_idvclas.py $dataset $nvoxel $nTR $exptype --loo $loo pha_em $niter $nfeat -r $rand --strfresh
            done
        done
    done
done
