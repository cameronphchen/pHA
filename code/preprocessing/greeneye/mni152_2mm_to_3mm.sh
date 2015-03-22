#!/bin/sh
# use fsl tool box to map auditory cortex mask and theory of mind mask from 
# MNI152 2mm to 3mm
# original masks are from neurosynth.org with keywork auditory cortex and 
# theory mind reverse map

mask_path=/jukebox/ramadge/RAW_DATA/green_eye
flirt -in $mask_path/masks/auditory_cortex_pFgA_z_FDR_0.01_reverse_2mm.nii.gz  \
      -ref $mask_path/niftis/MNI152_T1_3mm_brain_mask.nii \
      -applyxfm -usesqform -out $mask_path/masks/auditory_cortex_pFgA_z_FDR_0.01_reverse_3mm.nii.gz

flirt -in $mask_path/masks/theory_mind_pFgA_z_FDR_0.01_reverse_2mm.nii.gz  \
      -ref $mask_path/niftis/MNI152_T1_3mm_brain_mask.nii \
      -applyxfm -usesqform -out $mask_path/masks/theory_mind_pFgA_z_FDR_0.01_reverse_3mm.nii.gz

thresh=15
thresh_it="$(fslstats $mask_path/masks/auditory_cortex_pFgA_z_FDR_0.01_reverse_3mm.nii.gz -P $thresh)"
echo $thresh_it
fslmaths $mask_path/masks/auditory_cortex_pFgA_z_FDR_0.01_reverse_3mm.nii.gz -thr $thresh_it $mask_path/masks/auditory_cortex_mask_thr$thresh.nii.gz

thresh_it="$(fslstats $mask_path/masks/theory_mind_pFgA_z_FDR_0.01_reverse_3mm.nii.gz -P $thresh)"
echo $thresh_it
fslmaths $mask_path/masks/theory_mind_pFgA_z_FDR_0.01_reverse_3mm.nii.gz -thr $thresh_it $mask_path/masks/theory_mind_mask_thr$thresh.nii.gz

fslmaths $mask_path/masks/theory_mind_pFgA_z_FDR_0.01_reverse_3mm.nii.gz -add $mask_path/masks/auditory_cortex_pFgA_z_FDR_0.01_reverse_3mm.nii.gz \
    $mask_path/masks/ac_and_tom_pFgA_z_FDR_0.01_reverse_3mm.nii.gz

fslmaths $mask_path/masks/auditory_cortex_mask_thr$thresh.nii.gz -add $mask_path/masks/theory_mind_mask_thr$thresh.nii.gz \
     $mask_path/masks/ac_and_tom_mask_thr$thresh.nii.gz
