# image prediction experiment code

import numpy as np, sys
from scikits.learn.svm import NuSVC

def predict(transformed_data, args, trn_label ,tst_label):
  print 'imgpred',
  sys.stdout.flush()

  (ndim, nsample , nsubjs) = transformed_data.shape
  accu = np.zeros(shape=nsubjs)

  tst_data = np.zeros(shape = (ndim,nsample))
  trn_data = np.zeros(shape = (ndim,(nsubjs-1)*nsample))
  # image stimulus prediction 
  for tst_subj in range(nsubjs):
    tst_data = transformed_data[:,:,tst_subj]

    trn_subj = range(nsubjs)
    trn_subj.remove(tst_subj)

    for m in range(nsubjs-1):
      trn_data[:,m*56:(m+1)*56] = transformed_data[:,:,trn_subj[m]]

    # scikit-learn svm for classification
    clf = NuSVC(nu=0.5, kernel = 'linear')
    clf.fit(trn_data.T, trn_label)
    pred_label = clf.predict(tst_data.T)
      
    accu[tst_subj] = sum(pred_label == tst_label)/float(len(pred_label))

  return accu


