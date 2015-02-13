# forming transformation matrices for non loo experiment

import numpy as np
from scipy import stats

def form_transformation_matrix_loo(args, workspace_lh ,workspace_rh, align_data_lh, align_data_rh, nsubjs):
  transform_lh = np.zeros((args.nvoxel,args.nfeature,nsubjs))
  transform_rh = np.zeros((args.nvoxel,args.nfeature,nsubjs))
  
  loo = args.loo
  loo_idx = range(nsubjs)
  loo_idx = np.delete(loo_idx, loo)

  align_data_lh_loo_zscore = stats.zscore(align_data_lh[:,:,loo].T ,axis=0, ddof=1).T 
  align_data_rh_loo_zscore = stats.zscore(align_data_rh[:,:,loo].T ,axis=0, ddof=1).T

  if args.align_algo in ['ha']:
    bW_lh = workspace_lh['R']
    bW_rh = workspace_rh['R']
    for m in range(nsubjs-1):
      transform_lh[:,:,loo_idx[m]] = bW_lh[:,:,m]
      transform_rh[:,:,loo_idx[m]] = bW_rh[:,:,m]
    # find transform_lh[:,:,loo], transform_rh[:,:,loo]
    U_lh, s_lh, V_lh = np.linalg.svd(align_data_lh_loo_zscore.dot(workspace_lh['G']), full_matrices=False)
    U_rh, s_rh, V_rh = np.linalg.svd(align_data_rh_loo_zscore.dot(workspace_rh['G']), full_matrices=False)
    transform_lh[:,:,loo] = U_lh.dot(V_lh)
    transform_rh[:,:,loo] = U_rh.dot(V_rh)

  elif args.align_algo in ['pha_em','spha_vi']:
    bW_lh = workspace_lh['bW']
    bW_rh = workspace_rh['bW']
    for m in range(nsubjs-1):
      transform_lh[:,:,loo_idx[m]] = bW_lh[m*args.nvoxel:(m+1)*args.nvoxel,:]
      transform_rh[:,:,loo_idx[m]] = bW_rh[m*args.nvoxel:(m+1)*args.nvoxel,:]
    # find transform_lh[:,:,loo], transform_rh[:,:,loo]
    U_lh, s_lh, V_lh = np.linalg.svd(align_data_lh_loo_zscore.dot(workspace_lh['ES'].T), full_matrices=False)
    U_rh, s_rh, V_rh = np.linalg.svd(align_data_rh_loo_zscore.dot(workspace_rh['ES'].T), full_matrices=False)
    transform_lh[:,:,loo] = U_lh.dot(V_lh)
    transform_rh[:,:,loo] = U_rh.dot(V_rh)

  elif args.align_algo in ['ppca','pica']:
    bW_lh = workspace_lh['R']
    bW_rh = workspace_rh['R']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh
      transform_rh[:,:,m] = bW_rh

  elif args.align_algo == 'noalign' :
    for m in range(nsubjs):
      transform_lh[:,:,m] = np.identity(args.nvoxel)
      transform_rh[:,:,m] = np.identity(args.nvoxel)

  else :
    exit('alignment algo not recognized')

  return (transform_lh, transform_rh)
