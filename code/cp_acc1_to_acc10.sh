
exp='/jukebox/fastscratch/pohsuan/pHA/data/working/raider/1300vx/2203TR/mysseg_2nd_winsize9'


for nfeat in 10 50 100 500 1300
do 
	for rand in $(seq 0 4)
	do
		cp -i $exp/pica/${nfeat}feat/rand$rand/all/pica_acc_1.npz  \
                      $exp/pica/${nfeat}feat/rand$rand/all/pica_acc_10.npz
                for loo in $(seq 0 9)
                do
	        	cp -i $exp/pica/${nfeat}feat/rand$rand/loo$loo/pica_acc_1.npz  \
                              $exp/pica/${nfeat}feat/rand$rand/loo$loo/pica_acc_10.npz
                done
        done
        cp  -i $exp/ppca/${nfeat}feat/identity/all/ppca_acc_1.npz  \
               $exp/ppca/${nfeat}feat/identity/all/ppca_acc_10.npz
        for loo in $(seq 0 9)
        do
            cp  -i $exp/ppca/${nfeat}feat/identity/loo$loo/ppca_acc_1.npz  \
                   $exp/ppca/${nfeat}feat/identity/loo$loo/ppca_acc_10.npz
        done
done
