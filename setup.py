import os
from helpjson import *


if not os.path.isdir('./images_id'):
    os.system('wget -O images.zip https://www.dropbox.com/s/057aap4paild1zn/images_id.zip?dl=1')
    os.system('unzip images.zip')

model = ''
data2 = []

if not os.path.isfile('data_eval.json'):
    data = get_json('data_small.json')
    for d in data:
        for region in d['regions']:
            if region['phrase']['ln']['ln_pred']:
                data2.append(d)
                break
else:
    file = get_json('data_eval.json') 
    if 'data' not in file:
        model = 'Johnson et al. (2015)'
        data2 = get_json('data_eval.json')

        new_data = {'model': model, 'data': data2}
        save_json('data_eval.json', new_data)
