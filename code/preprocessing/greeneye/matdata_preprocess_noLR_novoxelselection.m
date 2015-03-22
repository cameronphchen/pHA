%function matdata_preprocess(nvoxel_str, nTR_str)

% please put compute_voxel_ranks.m under the same directory
%nTR_str = '449'
%nvoxel_str = '3427'
dataset = 'greeneye_ac_noLR'

%nTR = str2num(nTR_str)
%nvoxel = str2num(nvoxel_str)

load('/jukebox/ramadge/pohsuan/pHA/data/raw/greeneye_ac_noLR/greeneye_movie_ac_noLR.mat')

nsubjs = size(movie_all,1);
nvoxel = size(movie_all{1,1},1);
nTR    = size(movie_all{1,1},2);

movie_all
for i = 1:nsubjs
    movie_all{i,1}(all(movie_all{i,1}==0,2),:) = [];
end
movie_all

% computing voxel ranks for selection
movie_data = nan(nvoxel, nTR, nsubjs);
for i = 1:nsubjs
    movie_data(:,:,i) = movie_all{i,1};
end

assert(sum(sum(sum(isnan(movie_data)))) == 0)
assert(sum(sum(sum(~movie_data))) == 0)

output_path = ['/jukebox/ramadge/pohsuan/pHA/data/input/' dataset '/' nvoxel_str 'vx/' nTR_str 'TR/']

%mkdir(output_path)
%save([output_path 'movie_data_novxsel.mat'],'movie_data');

