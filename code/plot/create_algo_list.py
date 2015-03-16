import pickle

algo_list = []

algo = {'name': 'HA (850)',
  'align_algo': 'ha',
  'nfeature': '850',
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
  'name': 'pHAc 400',
  'align_algo': 'ha_syn',
  'nfeature': '400',
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
  'name': 'pHAc 600',
  'align_algo': 'ha_syn',
  'nfeature': '600',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)

algo = {
  'name': 'pHAc 700',
  'align_algo': 'ha_syn',
  'nfeature': '700',
  'kernel': None,
  'rand': True
}
algo_list.append(algo)


algo = {
  'name': 'pHAc 850',
  'align_algo': 'ha_syn',
  'nfeature': '850',
  'kernel': None,
  'rand': True
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
