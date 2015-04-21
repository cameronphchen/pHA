import pickle

algo_list = []


algo = {'name': 'MNI 152',
  'align_algo': 'noalign',
  'nfeature': '873',
  'kernel': None,
  'rand': False
}
algo_list.append(algo)

algo = {'name': 'HA (873)',
  'align_algo': 'ha',
  'nfeature': '873',
  'kernel': None,
  'rand': False
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
  'name': 'pHAc 200',
  'align_algo': 'ha_syn',
  'nfeature': '200',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 400',
  'align_algo': 'ha_syn',
  'nfeature': '400',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 873',
  'align_algo': 'ha_syn',
  'nfeature': '873',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)


"""
algo = {
  'name': 'spha_vi 10',
  'align_algo': 'spha_vi',
  'nfeature': '10',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'spha_vi 50',
  'align_algo': 'spha_vi',
  'nfeature': '50',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'spha_vi 100',
  'align_algo': 'spha_vi',
  'nfeature': '100',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)
"""

# write python dict to a file
output = open('algo_list.pkl', 'wb')
pickle.dump(algo_list, output)
output.close()

# read python dict back from the file
pkl_file = open('algo_list.pkl', 'rb')
algo_list_out = pickle.load(pkl_file)
pkl_file.close()

print algo_list
