
import skimage.io as io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from helpjson import load_json, save_json
import json
import collections

class AvaliacaoModel():
    
    def __init__(self):
        self.data = None
        self.current_key = None
        self.number_to_positions = dict()

        self.key_to_index = dict()
        self.index_to_key = dict()
        self.index        = 0

        self.name_file = None
    
    def build_number_to_positions(self):
        for i, k in enumerate(self.data.keys()):
            self.key_to_index[k] = i
            self.index_to_key[i] = k
        
        self.current_key = next(iter(self.data))
        self.index       = 0
    
    def load_phrases(self):
        region = self.curret_region()

        reference_nl      = region['phrase']['reference']
        baseline          = region['phrase']['baseline']
        predicted_model1  = region['phrase']['anon']
        predicter_model2  = region['phrase']['anonc']

        best_model        = region['phrase']['best_model']
        
        try:
            observation  = region['phrase']['observation']
        except KeyError:
            observation  = ''
        
        return reference_nl, baseline, predicted_model1, predicter_model2, observation, best_model
    
    def load_information(self, region, option, default = ''):
        return default if option not in region['phrase'] else region['phrase'][option]

    def load_combos(self):
        region = self.curret_region()

        option_baseline      = self.load_information(region, 'option_baseline')
        option_model1        = self.load_information(region, 'option_model1')
        option_model2        = self.load_information(region, 'option_model2')

        option_better_model1 = self.load_information(region, 'better_model1')
        option_better_model2 = self.load_information(region, 'better_model2')

        ignore               = self.load_information(region, 'ignore', default = 0)
        
        return ignore, option_baseline, option_model1, option_model2, option_better_model1, option_better_model2

    def draw_bbox(self, ax, bbox, edge_color='red', line_width =3):
        bbox_plot = mpatches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3],
            fill = False, edgecolor = edge_color, linewidth = line_width)
        ax.add_patch(bbox_plot)

    def load_image(self):
        region = self.curret_region()

        bbox = [region['x'], region['y'], region['width'], region['height']]
        path_image = 'images/{}.jpg'.format(self.current_key)

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
    
    def save_json(self):
        save_json(self.name_file, self.data)

    def save_observation(self, value):
        region = self.curret_region()
        
        if value.endswith('\n\n'):
            region['phrase']['observation'] = value[0:len(value)-2]
        else:
            if value == '\n':
                region['phrase']['observation'] = ''
            else:
                region['phrase']['observation'] = value
    
    def save_informations(self, ignore, model1, model2, best_model, observation, option_baseline, option_model1, option_model2):
        self.save_observation(observation)
        region = self.curret_region()
        
        region['phrase']['ignore']        = ignore

        region['phrase']['better_model1'] = model1
        region['phrase']['better_model2'] = model2
        region['phrase']['best_model'] = best_model
        
        region['phrase']['option_baseline'] = option_baseline
        region['phrase']['option_model1'] = option_model1
        region['phrase']['option_model2'] = option_model2

    def curret_region(self):
        return self.data[self.current_key]
    
    def go_to_key(self, key):
        assert key in self.key_to_index
        
        self.index = self.key_to_index[key]
        self.current_key = key
    
    def go_to_instance(self, number_instance):
        assert number_instance >= 0 and number_instance <= len(self.data)-1
    
        self.current_key = list(self.data.keys())[number_instance]
        self.index = number_instance

    def previous_example(self):
        try:
            self.go_to_instance(self.index - 1)
        except:
            pass

    def next_instance(self):
        try:
            self.go_to_instance(self.index + 1)
        except:
            pass