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
    transform_lh_tmp = workspace_lh['R']
    transform_rh_tmp = workspace_rh['R']
    for m in range(transform_lh_tmp.shape[2]):
      transform_lh[:,:,loo_idx[m]] = transform_lh_tmp[:,:,m]
      transform_rh[:,:,loo_idx[m]] = transform_rh_tmp[:,:,m]
    # find transform_lh[:,:,loo], transform_rh[:,:,loo]
    U_lh, s_lh, V_lh = np.linalg.svd(align_data_lh_loo_zscore.dot(workspace_lh['G']), full_matrices=False)
    U_rh, s_rh, V_rh = np.linalg.svd(align_data_rh_loo_zscore.dot(workspace_rh['G']), full_matrices=False)
    transform_lh[:,:,loo] = U_lh.dot(V_lh)
    transform_rh[:,:,loo] = U_rh.dot(V_rh)
  elif args.align_algo in ['pha_em','spha_vi']:
    transform_lh_tmp = workspace_lh['bW']
    transform_rh_tmp = workspace_rh['bW']
    for m in range(transform_lh_tmp.shape[2]):
      transform_lh[:,:,loo_idx[m]] = transform_lh_tmp[m*args.nvoxel:(m+1)*args.nvoxel,:]
      transform_rh[:,:,loo_idx[m]] = transform_rh_tmp[m*args.nvoxel:(m+1)*args.nvoxel,:]
    # find transform_lh[:,:,loo], transform_rh[:,:,loo]
    U_lh, s_lh, V_lh = np.linalg.svd(align_data_lh_loo_zscore.dot(workspace_lh['ES'].T), full_matrices=False)
    U_rh, s_rh, V_rh = np.linalg.svd(align_data_rh_loo_zscore.dot(workspace_rh['ES'].T), full_matrices=False)
    transform_lh[:,:,loo] = U_lh.dot(V_lh)
    transform_rh[:,:,loo] = U_rh.dot(V_rh)
  elif args.align_algo in ['ppca','pica']:
    transform_lh_tmp = workspace_lh['R']
    transform_rh_tmp = workspace_rh['R']
    for m in range(nsubjs):
      transform_lh[:,:,m] = bW_lh
      transform_rh[:,:,m] = bW_rh
  elif args.align_algo == 'None' :
    for m in range(nsubjs):
      transform_lh[:,:,m] = np.identity(args.nvoxel)
      transform_rh[:,:,m] = np.identity(args.nvoxel)
  else :
    exit('alignment algo not recognized')


  return (transform_lh, transform_rh)
