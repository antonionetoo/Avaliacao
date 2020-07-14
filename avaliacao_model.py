import collections
import random

import skimage.io as io

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from helpjson import load_json, save_json

class AvaliacaoModel():
    
    def __init__(self):
        self.data = None
        self.current_key = None
        self.number_to_positions = dict()

        self.key_to_index = dict()
        self.index_to_key = dict()
        self.index        = 0

        self.name_file = None
        
        self.models = {0: ['phrase_joao', 'option_joao'],
                       1: ['phrase_antonio', 'option_antonio'],
                       2: ['baseline_joao', 'option_bjoao'],
                       3: ['baseline_antonio', 'option_bantonio'],}
        
        self.order_models = [0, 1, 2, 3]
        self.best_model = ['Nenhum', 'Modelo 1', 'Modelo 2', 'Modelo 3', 'Modelo 4']
    
    def build_number_to_positions(self):
        for i, k in enumerate(self.data.keys()):
            self.key_to_index[k] = i
            self.index_to_key[i] = k
        
        self.current_key = next(iter(self.data))
        self.index       = 0
    
    def order(self, n):
        return self.order_models[n]
    
    def name_phrase(self, name):
        return self.models[self.order(name)][0]

    def name_option_by_index(self, index):
        return self.models[self.order_models[index]][1]

    def name_option(self, name):
        return (name if name == 'Nenhum' else self.name_option_by_index(int(name[-1]) - 1 ))
    
    def load_phrases(self):
        region = self.curret_region()
        
        predicted_model1 = region[self.name_phrase(0)]
        predicted_model2 = region[self.name_phrase(1)]
        predicted_model3 = region[self.name_phrase(2)]
        predicted_model4 = region[self.name_phrase(3)]
                                
        try:
            observation = region['observation']
        except KeyError:
            observation = ''
        
        return predicted_model1, predicted_model2, predicted_model3, predicted_model4, observation
    
    def load_information(self, region, option, default = ''):
        return default if option not in region else region[option]

    def load_combos(self):
        region = self.curret_region()

        option_model1  = self.load_information(region, self.name_option_by_index(0))
        option_model2  = self.load_information(region, self.name_option_by_index(1))
        option_model3  = self.load_information(region, self.name_option_by_index(2))
        option_model4  = self.load_information(region, self.name_option_by_index(3))
        
        best_model = ''
        if 'best_model' in region and not region['best_model'] == 'Nenhum':
            index = [i for i, m in enumerate(self.models.values()) if m[1] == region['best_model']][0]
            best_model = 'Modelo ' + str([e for e, o in enumerate(self.order_models) if o == index][0] + 1)

        return option_model1, option_model2, option_model3, option_model4, best_model

    def draw_bbox(self, ax, bbox, edge_color='red', line_width =3):
        bbox_plot = mpatches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3],
            fill = False, edgecolor = edge_color, linewidth = line_width)
        ax.add_patch(bbox_plot)

    def load_image(self):
        region = self.curret_region()

        bbox = [region['x'], region['y'], region['width'], region['height']]
        path_image = 'images_linkpics/{}.jpg'.format(region['image'].split('.')[0])

        plt.close('all')

        img = io.imread(path_image)
        fig = plt.figure()
        
        plt.imshow(img)

        ax = plt.gca()
        self.draw_bbox(ax, bbox)

        return fig

    def load_json(self, name_file):
        self.data = collections.OrderedDict(sorted(load_json(name_file).items()))
        self.name_file = name_file
        
        self.build_number_to_positions()
    
    def save_json(self):
        save_json(self.name_file, self.data)

    def save_observation(self, value):
        region = self.curret_region()
        
        if value.endswith('\n\n'):
            region['observation'] = value[0:len(value)-2]
        else:
            if value == '\n':
                region['observation'] = ''
            else:
                region['observation'] = value
        
    def save_informations(self, best_model, observation, option_model1, option_model2, option_model3, option_model4):
        self.save_observation(observation)
        region = self.curret_region()

        region['best_model']  = self.name_option(best_model)
        
        region[self.name_option_by_index(0)] = option_model1
        region[self.name_option_by_index(1)] = option_model2
        region[self.name_option_by_index(2)] = option_model3
        region[self.name_option_by_index(3)] = option_model4

    def curret_region(self):
        return self.data[self.current_key]
    
    def go_to_key(self, key):
        random.shuffle(self.order_models)
        assert key in self.key_to_index
        
        self.index = self.key_to_index[key]
        self.current_key = key
    
    def go_to_instance(self, number_instance):
        random.shuffle(self.order_models)
        assert number_instance >= 0 and number_instance <= len(self.data)-1
    
        self.current_key = list(self.data.keys())[number_instance]
        self.index = number_instance

    def previous_example(self):
        self.go_to_instance(self.index - 1)

    def next_instance(self):
        self.go_to_instance(self.index + 1)

