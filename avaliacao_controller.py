from avaliacao_model import AvaliacaoModel
from avaliacao_view import TelaAvaliacao

from tkinter import constants
from tkinter import filedialog
from tkinter import messagebox

class ControllerAvaliacao():

    def __init__(self):
        self.model = AvaliacaoModel()
        self.view = TelaAvaliacao(self)

    def enter_instance_number(self, event):
        self.save_informations()
        n_instance = int(self.view.txt_num_exemplo.get())
        
        try:
            self.model.go_to_instance(n_instance)
            self.load_informations()
        except:
            messagebox.showinfo("Erro", "Exemplo não encontrado")

    def enter_identifier(self, event):
        self.save_informations()
        key = self.view.txt_identifier.get()
        
        try:
            self.model.go_to_key(key)
            self.load_informations()
        except:
            messagebox.showinfo("Erro", "Exemplo não encontrado")

    def save_file(self):
        self.save_informations()
        self.model.save_json()

    def file_open(self):
        mask = [("Arquivos json","*.json")]
        f = filedialog.askopenfile(filetypes=mask, mode='r')

        if f == None:
            return 
        
        name_file = f.name
        self.model.load_json(name_file)

        self.model.build_number_to_positions()
        self.load_informations()
    
    def save_informations(self):
        model1      = self.view.better_model1.get()
        model2      = self.view.better_model2.get()
        best_model  = self.view.best_model.get()
        observation = self.view.txt_observacao.get("1.0", constants.END)
        
        option_baseline = self.view.combo_baseline.get()
        option_model1   = self.view.combo_model1.get()
        option_model2   = self.view.combo_model2.get()
        
        
        self.model.save_informations(model1, model2, best_model, observation, option_baseline, option_model1, option_model2)
    
    def load_phrase(self, txt, value):
        txt.delete(0, constants.END)
        txt.insert(0, value)

    def load_phrases(self):
        reference_nl, baseline, predicted_model1, predicter_model2, observation, model1, model2, best_model = self.model.load_phrases()

        self.load_phrase(self.view.txt_reference, reference_nl)
        self.load_phrase(self.view.txt_baseline, baseline)
        self.load_phrase(self.view.txt_model1, predicted_model1)
        self.load_phrase(self.view.txt_model2, predicter_model2)
        self.load_phrase(self.view.txt_identifier, self.model.current_key)
        
        self.view.txt_observacao.delete(1.0, constants.END)
        self.view.txt_observacao.insert(constants.END, observation)
        
        self.view.better_model1.set(model1 or 0)
        self.view.better_model2.set(model2 or 0)
        self.view.best_model.set(best_model or 0)
        
        self.load_phrase(self.view.txt_num_exemplo, self.model.index)
        
        option_baseline, option_model1, option_model2 = self.model.load_combos()
        
        self.view.combo_baseline.set(option_baseline)
        self.view.combo_model1.set(option_model1)
        self.view.combo_model2.set(option_model2)

    def load_informations(self):
        self.view.plot_image(self.model.load_image())
        self.load_phrases()
        
    def previous_example(self):
        self.save_informations()
        self.model.previous_example()

        self.load_informations()
    
    def next_instance(self):
        self.save_informations()
        self.model.next_instance()

        self.load_informations()

    def start(self):
        self.view.show_interface()