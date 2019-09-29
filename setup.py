import os
from helpjson import *

#os.system('wget ')


data = get_json('data_small.json')
data2 = []
for d in data:
    for region in d['regions']:
        if region['phrase']['ln']['ln_pred']:
            data2.append(d)
            break

save_json('data_eval.json', data2)