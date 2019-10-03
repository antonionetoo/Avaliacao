import os
from helpjson import *

path_file = ''
if os.path.isfile('data_eval.json'):
    path_file = 'data_eval.json'
else:
    path_file = 'data_small.json'

file  = get_json(path_file)
model = ''

if 'model' in file:
    data = file['data']
    model = file['model']
else:
    data = file
    model = 'Não identificado'

data2 = []
for d in data:
    ad = False
    regions = []

    for i, region in enumerate(d['regions']):
        if region['phrase']['ln']['ln_pred']:
            ad = True
            regions.append(region)

        elif not region['phrase']['ln']['ln_pred'] and ad == True: 
            x      = min(regions[-1]['x'], region['x'])
            y      = min(regions[-1]['y'], region['y'])

            x_bottom = max((regions[-1]['x'] + regions[-1]['width']), ((region['x'] + region['width'])))
            y_bottom = max((regions[-1]['y'] + regions[-1]['height']), ((region['y'] + region['height'])))

            width = x_bottom - x
            height = y_bottom - y

            regions[-1]['x'] = x
            regions[-1]['y'] = y
            regions[-1]['width'] = width
            regions[-1]['height'] = height
    if len(regions) > 0 :
        d['regions'] = regions
        data2.append(d)

new_data = {'model':model, 'data':data2}
save_json('data_eval.json', new_data)