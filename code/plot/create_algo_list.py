import pickle

algo_list = []

algo = {'name': 'noalign',
  'align_algo': 'noalign',
  'nfeature': '1300',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {'name': 'HA',
  'align_algo': 'ha',
  'nfeature': '1300',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'pHA I',
  'align_algo': 'pha_em',
  'nfeature': '1300',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)


algo = {
  'name': 'pHA 10',
  'align_algo': 'pha_em',
  'nfeature': '10',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHA 50',
  'align_algo': 'pha_em',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHA 100',
  'align_algo': 'pha_em',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHA 500',
  'align_algo': 'pha_em',
  'nfeature': '500',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHA 1300',
  'align_algo': 'pha_em',
  'nfeature': '1300',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 10',
  'align_algo': 'ha_syn',
  'nfeature': '10',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 50',
  'align_algo': 'ha_syn',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 100',
  'align_algo': 'ha_syn',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 500',
  'align_algo': 'ha_syn',
  'nfeature': '500',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 1300',
  'align_algo': 'ha_syn',
  'nfeature': '1300',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pPCA 10',
  'align_algo': 'ppca',
  'nfeature': '10',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'pPCA 50',
  'align_algo': 'ppca',
  'nfeature': '50',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'pPCA 100',
  'align_algo': 'ppca',
  'nfeature': '100',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'pPCA 500',
  'align_algo': 'ppca',
  'nfeature': '500',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {
  'name': 'pPCA 1300',
  'align_algo': 'ppca',
  'nfeature': '1300',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)


# write python dict to a file
output = open('algo_list.pkl', 'wb')
pickle.dump(algo_list, output)
output.close()

# read python dict back from the file
pkl_file = open('algo_list.pkl', 'rb')
algo_list_out = pickle.load(pkl_file)
pkl_file.close()

print algo_list
