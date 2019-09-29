from helpjson import *


data = get_json('data_small.json')
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
            
save_json('data_eval.json', data2)