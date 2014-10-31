#!/usr/bin/env python

#variational inference algorithm for semiparametric probabilistic Hyperalignment

#movie_data is a three dimensional matrix of size voxel x TR x nsubjs
#movie_data[:,:,m] is the data for subject m, which will be X_m^T in the standard 
#mathematic notation

# prior
# bK_i  : TR x TR

# Variational Parameters:
# mu_s  : nvoxel x TR
# Sig_s : TR x TR x nvoxel

# Hyperparameters:
# W_m   : nvoxel x nvoxel x nsubjs
# rho2  : nsubjs 
# mu    : nvoxel*nsubj 

import numpy as np, scipy, random, sys, math, os
from scipy import stats
import sys
sys.path.append('/jukebox/ramadge/pohsuan/pyGPs')
import pyGPs

def spHA_VI(movie_data, options, para, lrh):
  print 'spHA_VI'
  nvoxel = movie_data.shape[0]
  nTR    = movie_data.shape[1]
  nsubjs = movie_data.shape[2]

  align_algo = para['align_algo']

  current_file = options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_current.npz' 
  # zscore the data
  bX = np.zeros((nsubjs*nvoxel,nTR))
  for m in range(nsubjs):
    bX[m*nvoxel:(m+1)*nvoxel,:] = stats.zscore(movie_data[:,:,m].T ,axis=0, ddof=1).T

  del movie_data

  # initialization when first time run the algorithm
  if not os.path.exists(current_file):
    # prior
    #bK_i   = np.identity((nvoxel,nvoxel))

    kernel = pyGPs.cov.RBFard(1)
    T_idx  = np.arange(nTR)
    T_idx  = T_idx[:,None] 
    bK_i   = kernel.getCovMatrix(T_idx,T_idx,'train')  

    # variational parameters
    #          --bmu_{\bs_1}^T--
    # bmu_s =  --bmu_{\bs_n}^T-- 
    #          --bmu_{\bs_N}^T--
    ES  = np.zeros((nvoxel,nTR))

    # hyperparameters
    bW      = np.zeros((nsubjs*nvoxel,nvoxel))
    bmu     = np.zeros(nvoxel*nsubjs)
    sigma2  = np.zeros(nsubjs)
    btheta  = kernel.hyp 
  
    for m in range(nsubjs):
      bW[m*nvoxel:(m+1)*nvoxel,:] = np.identity(nvoxel) 
      bmu[m*nvoxel:(m+1)*nvoxel] = np.mean(bX[m*nvoxel:(m+1)*nvoxel,:],1)
      sigma2[m] = 1

      #initialize K
    niter = 0
    np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(para['nvoxel'])+'vx_'+str(niter)+'.npz',\
                                bW = bW, bmu=bmu, sigma2=sigma2, ES=ES, btheta = btheta , niter=niter)

  # more iterations starts from previous results
  else:
    workspace = np.load(current_file)
    niter = workspace['niter']
    workspace = np.load(options['working_path']+align_algo+'_'+lrh+'_'+str(para['nvoxel'])+'vx_'+str(niter)+'.npz')
    bW     = workspace['bW']
    bmu    = workspace['bmu']
    sigma2 = workspace['sigma2']
    ES     = workspace['ES']
    niter  = workspace['niter']

  # remove mean
  bX = bX - bX.mean(axis=1)[:,np.newaxis]

  print str(niter+1)+'th',
  for it in range(para['niter_unit']):
    sys.stdout.flush()
    tmp_sum_tr_Sig_si = 0
    Sig_si_sum = np.zeros((nTR,nTR))
    mumuT_sum  = np.zeros((nTR,nTR))
    tmp_log_det_Sigsi = 0
    for i in range(nvoxel):
      print i,
      sys.stdout.flush()

      tmp_sig_si = 0    
      # calculate \bSig_{\bs_i} 
      for m in range(nsubjs):
        tmp_sig_si += ( np.linalg.norm(bW[m*nvoxel:(m+1)*nvoxel,i])**2 )/sigma2[m]
      Sig_si =  scipy.linalg.inv( scipy.linalg.inv(bK_i) + tmp_sig_si*np.identity(nTR) )
      #tmp_log_det_Sigsi += math.log(np.linalg.det(Sig_si))
      sign , tmp_log_det_Sigsi = np.linalg.slogdet(Sig_si)
      if sign == -1:
        print str(new_niter)+'th iteration, log sign negative'
      Sig_si_sum += Sig_si
      tmp_sum_tr_Sig_si += np.trace(Sig_si)
      # calculate \bmu_{\bs_i}
      tmp_sigma2WxWE = np.zeros((nTR,1)) 
      for m in range(nsubjs):
        print('.'),
        sys.stdout.flush()
        tmp_WxWE = np.zeros((nTR,1))
        for k in range(nvoxel):
          tmp_WmkjEsj = np.zeros((nTR,1))
          for j in range(nvoxel):
            if j == i: continue
            tmp_WEST = bW[m*nvoxel+k,j]*ES[j,:].T
            tmp_WEST = tmp_WEST[:,None] 
            tmp_WmkjEsj += tmp_WEST
          tmp_bX_k = bX[m*nvoxel+k,:].T
          tmp_bX_k = tmp_bX_k[:,None] 
          tmp_WxWE += bW[m*nvoxel+k,i]*( tmp_bX_k- tmp_WmkjEsj)
        tmp_sigma2WxWE += tmp_WxWE/sigma2[m]
      ES[i,:]   = (Sig_si.dot(tmp_sigma2WxWE)).T
      mumuT_sum += np.outer(ES[i,:],ES[i,:]) 

    print m,
    for m in range(nsubjs):
      print('.'),
      sys.stdout.flush()
      Am = bX[m*nvoxel:(m+1)*nvoxel,:].dot(ES.T)
      Um, sm, Vm = np.linalg.svd(Am+0.00001*np.eye(nvoxel))
      bW[m*nvoxel:(m+1)*nvoxel,:] = Um.dot(Vm)
      tmp_sigma2 = 0
      for i in range(nvoxel):
        tmp_sigma2 +=   np.trace(bX[m*nvoxel:(m+1)*nvoxel,:].T.dot(bX[m*nvoxel:(m+1)*nvoxel,:])) \
                    -2*np.trace(ES.T.dot(bW[m*nvoxel:(m+1)*nvoxel,:].T).dot(bX[m*nvoxel:(m+1)*nvoxel,:]))\
                    +  np.trace(ES.dot(ES.T)) + tmp_sum_tr_Sig_si
      sigma2[m] = nTR / tmp_sigma2

    bK_i_inv = scipy.linalg.inv(bK_i) 
    for l in range(len(betheta)):
      btheta[l]+=-0.5*np.trace(bK_i_inv.dot(nvoxel*bK_i + mumuT_sum - bSig_si_sum).dot(bK_i_inv)\
                          .dot( kernel.getDerMatrix( T_idx,T_idx, 'train',l ) ))

    new_niter = niter + para['niter_unit']
    np.savez_compressed(current_file, niter = new_niter)  
    np.savez_compressed(options['working_path']+align_algo+'_'+lrh+'_'+str(nvoxel)+'vx_'+str(new_niter)+'.npz',\
                              bW = bW, bmu=bmu, sigma2=sigma2, btheta = btheta, ES=ES, niter=new_niter)
  
    # calculate ELBO
    tmp_2rho2XmTXm = 0
    tmp_rho2WmTXm = 0
    tmp_1over2rho2 = 0
    for m in range(nsubjs):
      tmp_2rho2XmTXm += np.trace(bX[m*nvoxel:(m+1)*nvoxel,:].T.dot(bX[m*nvoxel:(m+1)*nvoxel,:]))/(2*sigma2[m])  
      tmp_rho2WmTXm += np.trace(ES.T.dot(bW[m*nvoxel:(m+1)*nvoxel,:].T).dot(bX[m*nvoxel:(m+1)*nvoxel,:]))/sigma2[m]
      tmp_1over2rho2 += 1/(2*sigma2[m])

    tmp_muKmu = 0
    tmp_trKSig = 0
    for i in range(nvoxel):
      tmp_muKmu  += ES[i,:].T.dot(bK_i_inv).dot(E[i,:])
      tmp_trKSig += np.trace(bK_i_inv.dot(Sig_si_sum))

    ELBO = nTR*nvoxel*np.sum(sigma2)/2 - tmp_2rho2XmTXm + tmp_rho2WmTXm - tmp_1over2rho2*np.trace(ES.T.dot(ES))\
        -tmp_1over2rho2*Sig_si_sum -0.5*N*math.log(np.linalg.det(bK_i)) - 0.5*tmp_muKmu - 0.5*tmp_trKSig - 0.5*tmp_log_det_Sigsi

    print it,
    print ELBO

    np.savez_compressed(options['output_path']+align_algo+'_'+'elbo_'+lrh+'_'+str(nvoxel)+'vx_'+str(new_niter)+'.npz',\
                   ELBO=ELBO)

  return new_niter
