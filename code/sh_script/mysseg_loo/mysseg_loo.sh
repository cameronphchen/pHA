#!/bin/sh

#usage: run_exp.py dataset nvoxel nTR  exptype [-l, --loo] [-e, --expopt] [-w, --winsize] 
#             align_algo [-k kernel] niter nfeature [-r RANDSEED] [--strfresh]

dataset='raider'
nvoxel=1300
nTR=2203
winsize=9
ln -s /jukebox/ramadge/pohsuan/pHA/code/run_exp.py run_exp.py
chmod +x run_exp.py
for loo in  $(seq 0 9)
do

  #submit      run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize noalign 10 1300 --strfresh
  #submit      run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize noalign 10 1300 --strfresh
  #submit_long run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize pha_em 10 1300 --strfresh
  #submit_long run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize pha_em 10 1300 --strfresh
  #submit_long run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize ha 10 1300 --strfresh
  #submit_long run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize ha 10 1300 --strfresh

    for nfeat in 10  50 100 500 1300
    do 
    #submit run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize ppca 10 $nfeat --strfresh
    #submit run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize ppca 10 $nfeat --strfresh    
        for rand in   $(seq 0 4)
        do
            #submit      run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize pica 1 $nfeat -r $rand --strfresh
            #submit      run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize pica 1 $nfeat -r $rand --strfresh
            #submit run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize ha_syn 10 $nfeat -r $rand --strfresh
            #submit run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize ha_syn 10 $nfeat -r $rand --strfresh
            submit_long run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize ha_sm_retraction 10 $nfeat -r $rand --strfresh
            submit_long run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize ha_sm_retraction 10 $nfeat -r $rand --strfresh
            #pni_submit -q long.q -P long -l vf=20G run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 1st -w $winsize pha_em 10 $nfeat -r $rand --strfresh
            #pni_submit -q long.q -P long -l vf=20G run_exp.py $dataset $nvoxel $nTR mysseg --loo $loo -e 2nd -w $winsize pha_em 10 $nfeat -r $rand --strfresh
        done
    done
done
