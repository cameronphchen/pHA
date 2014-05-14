%function matdata_preprocess(nvoxel_str, nTR_str)

% please put compute_voxel_ranks.m under the same directory
nTR_str = '2203'
nvoxel_str = '1300'

nTR = str2num(nTR_str)
nvoxel = str2num(nvoxel_str)

load ../data/input/movie_data_princeton;
load ../data/input/vt_masks_lhrh;
load ../data/input/monkeydog_timeaveraged_data.mat
load ../data/input/block_labels.txt

mkdir(['../data/working/' int2str(nTR) 'TR/'])
mkdir(['../data/output/' int2str(nTR) 'TR/'])
mkdir(['/fastscratch/pohsuan/pHA/data/working/' int2str(nTR) 'TR/'])


for subj_index = 1:size(movie_data_raw_despiked,1)
    mv_data = movie_data_raw_despiked{subj_index,1};
    if nTR == 2203
      mv_data = [mv_data(:,5:1101), mv_data(:,1102+5:2212)];
    else
      mv_data = [mv_data(:,5:nTR+4)];
    end
    movie_data_raw_despiked(subj_index,1) = {mv_data};
end

nsubjs = size(movie_data_raw_despiked,1);

% computing voxel ranks for selection
fprintf('start voxel rank \n')
vox_ranks = cell(2,1);
for h = 1:2
    data = cell(nsubjs,1);
    for i = 1:nsubjs
        data(i,1) = {movie_data_raw_despiked{i,1}(vt_mask{i,1}==h,:)'};
    end 
    [vox_corr_ranks] = compute_voxel_ranks(data,0);
    vox_ranks(h,1) = {vox_corr_ranks};
end
fprintf('end voxel rank \n')


% save movie data to file
movie_data_lh = nan(nvoxel, nTR, nsubjs);
movie_data_rh = nan(nvoxel, nTR, nsubjs);
for i = 1:nsubjs
    data_temp = movie_data_raw_despiked{i,1}(vt_mask{i,1}==1,:);
    movie_data_lh(:,:,i) = data_temp(vox_ranks{1,1}{i,1}(1:nvoxel),:);
    data_temp = movie_data_raw_despiked{i,1}(vt_mask{i,1}==2,:);
    movie_data_rh(:,:,i) = data_temp(vox_ranks{2,1}{i,1}(1:nvoxel),:);
end

assert(sum(sum(sum(isnan(movie_data_rh)))) == 0)
assert(sum(sum(sum(isnan(movie_data_lh)))) == 0)


save(['/fastscratch/pohsuan/pHA/data/working/' int2str(nTR) 'TR/movie_data_lh_' int2str(nvoxel) 'vx.mat'],'movie_data_lh');
save(['/fastscratch/pohsuan/pHA/data/working/' int2str(nTR) 'TR/movie_data_rh_' int2str(nvoxel) 'vx.mat'],'movie_data_rh');


% apply voxel selection on image watching data
mkdg_data_lh = nan(nvoxel, 56, nsubjs);
mkdg_data_rh = nan(nvoxel, 56, nsubjs);
for i = 1:nsubjs
    data_tmp = mkdg_timeaveraged_data{i,1};

    mkdg_data_lh_tmp = data_tmp(vt_mask{i,1}==1,:);
    mkdg_data_rh_tmp = data_tmp(vt_mask{i,1}==2,:);

    mkdg_data_lh_tmp = mkdg_data_lh_tmp(vox_ranks{1,1}{i,1}(1:nvoxel),:);
    mkdg_data_rh_tmp = mkdg_data_rh_tmp(vox_ranks{2,1}{i,1}(1:nvoxel),:);

%    mkdg_data_lh_tmp = mkdg_data_lh_tmp(1:nvoxel,:);
%    mkdg_data_rh_tmp = mkdg_data_rh_tmp(1:nvoxel,:);

    mkdg_data_lh_tmp = zscore(mkdg_data_lh_tmp')';
    mkdg_data_rh_tmp = zscore(mkdg_data_rh_tmp')';    

    mkdg_data_lh(:,:,i) = mkdg_data_lh_tmp(:,block_labels>0); 
    mkdg_data_rh(:,:,i) = mkdg_data_rh_tmp(:,block_labels>0);
end

assert(sum(sum(sum(isnan(mkdg_data_lh)))) == 0)
assert(sum(sum(sum(isnan(mkdg_data_rh)))) == 0)

save(['/fastscratch/pohsuan/pHA/data/working/' int2str(nTR) 'TR/mkdg_data_lh_' int2str(nvoxel) 'vx.mat'],'mkdg_data_lh');
save(['/fastscratch/pohsuan/pHA/data/working/' int2str(nTR) 'TR/mkdg_data_rh_' int2str(nvoxel) 'vx.mat'],'mkdg_data_rh');



%end
