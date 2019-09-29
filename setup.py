import os
from helpjson import *

os.system('wget -O images.zip https://www.dropbox.com/s/057aap4paild1zn/images_id.zip?dl=1')
os.system('unzip images.zip')

data = get_json('data_small.json')
data2 = []
for d in data:
    for region in d['regions']:
        if region['phrase']['ln']['ln_pred']:
            data2.append(d)
            break

save_json('data_eval.json', data2)