
class AvaliacaoModel():
    
    def __init__(self):
        self.data = None
        self.number_to_positions = dict()
        self.index = 0
        self.dir_file = None

    def save_observation(self, value):
        region = self.curret_region()
        region['phrase']['ln']['ln_observacao'] = value    

    def previous_example(self):
        if self.index > 0:
            self.index -= 1

    def curret_region(self):
        i = self.number_to_positions[self.index][0]
        j = self.number_to_positions[self.index][1]

        return self.data[i]['regions'][j]

    def load_image(self, region):
        bbox = [region['x'], region['y'], region['width'], region['height']]
        path_image = 'images_id/{}.jpg'.format(region['image_id'])

        plt.close('all')

        img = io.imread(path_image)
        fig = plt.figure()
        
        plt.imshow(img)

        ax = plt.gca()
        draw_bbox(ax, bbox)

        canvas = FigureCanvasTkAgg(fig, master = window)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 5, rowspan = 20, sticky = W+E)

    def load_phrase(self, key):
        return self.curret_region()['phrase']['ln'][key]

    def load_phrases(self):
        ln_ref      = self.load_phrase('ln_ref')
        ln_ref_anon = self.load_phrase('ln_ref_anon')
        ln_pred     = self.load_phrase('ln_pred')

        ln_observacao = None
        try:
            ln_observacao = self.load_phrase('ln_observacao')
        except KeyError:
            ln_observacao = ''

        return ln_ref, ln_ref_anon, ln_pred, ln_observacao

    def load_combo(self, key, default = ''):
        if key in self.curret_region()['phrase']['ln']:
            value = self.curret_region()['phrase']['ln'][key]
            if value == '' or value == None :
                self.curret_region()['phrase']['ln'][key] = None
                return default
            else:
                return value
        else:
            return default

    def load_combos(self):
        ln_ref_eval      = self.load_combo('ln_ref_eval', 'Correto')
        ln_ref_anon_eval = self.load_combo('ln_ref_anon_eval')
        ln_pred_eval     = self.load_combo('ln_pred_eval')

        return ln_ref_eval, ln_ref_anon_eval, ln_pred_eval

    def load_information(self):       
        #self.load_image(region)
        ln_ref, ln_ref_anon, ln_pred, ln_observacao = self.load_phrases()
        ln_ref_eval, ln_ref_anon_eval, ln_pred_eval = self.load_combos()

        return ln_ref, ln_ref_anon, ln_pred, ln_observacao, ln_ref_eval, ln_ref_anon_eval, ln_pred_eval, self.index
    
    def build_number_to_positions(self, data):
        self.data = data
        k = -1
        for i, d in enumerate(data):
            for j, _ in enumerate(d['regions']):
                k += 1
                self.number_to_positions[k] = [i, j]
        
        self.index = 0
    
    def next_instance(self):
        if self.index < len(self.number_to_positions) - 1:
            self.index += 1    
    
    def current_index(self):
        return self.index