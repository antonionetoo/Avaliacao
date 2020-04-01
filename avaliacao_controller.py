from avaliacao_model import AvaliacaoModel
from avaliacao_view import TelaAvaliacao

from tkinter import constants
from tkinter import filedialog
from tkinter import messagebox
from tkinter import constants

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
        ignore             = self.view.ignore.get()

        better_model1      = self.view.combo_better_model1.get()
        better_model2      = self.view.combo_better_model2.get()
        better_model3      = self.view.combo_better_model3.get()

        best_model  = self.view.best_model.get()
        observation = self.view.txt_observacao.get("1.0", constants.END)
        
        option_baseline = self.view.combo_baseline.get()
        option_model1   = self.view.combo_model1.get()
        option_model2   = self.view.combo_model2.get()
        option_model3   = self.view.combo_model3.get()
        
        self.model.save_informations(ignore, better_model1, better_model2, better_model3, best_model, observation, option_baseline, option_model1, option_model2, option_model3)
    
    def load_phrase(self, txt, value):
        txt.delete(0, constants.END)
        txt.insert(0, value)

    def load_phrases(self):
        reference_nl, baseline, predicted_model1, predicted_model2, predicted_model3, observation, best_model = self.model.load_phrases()

        self.load_phrase(self.view.txt_reference, reference_nl)
        self.load_phrase(self.view.txt_baseline, baseline)
        self.load_phrase(self.view.txt_model1, predicted_model1)
        self.load_phrase(self.view.txt_model2, predicted_model2)
        self.load_phrase(self.view.txt_model3, predicted_model3)
        self.load_phrase(self.view.txt_identifier, self.model.current_key)
        
        self.view.txt_observacao.delete(1.0, constants.END)
        self.view.txt_observacao.insert(constants.END, observation)
        
        self.view.best_model.set(best_model or 'Nenhum')
        
        self.load_phrase(self.view.txt_num_exemplo, self.model.index)
    
    def load_combos(self):
        ignore, option_baseline, option_model1, option_model2, option_model3, option_better_model1, option_better_model2, option_better_model3 = self.model.load_combos()
        
        self.view.combo_baseline.set(option_baseline)
        self.view.combo_model1.set(option_model1)
        self.view.combo_model2.set(option_model2)
        self.view.combo_model3.set(option_model3)

        self.view.combo_better_model1.set(option_better_model1)
        self.view.combo_better_model2.set(option_better_model2)
        self.view.combo_better_model3.set(option_better_model3)
        self.view.ignore.set(ignore)

    def load_informations(self):
        self.view.ignore.set(0)
        self.ignore()

        self.view.plot_image(self.model.load_image())
        self.load_phrases()
        self.load_combos()

        if self.view.ignore.get():
            self.ignore()
        
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
    
    def change_value_combo(self, combo, new_state):
        combo.set('')
        combo.config(state = new_state)

    def ignore(self):
        new_state = constants.DISABLED if self.view.ignore.get() else 'readonly'

        self.change_value_combo(self.view.combo_baseline, new_state)
        self.change_value_combo(self.view.combo_model1, new_state)
        self.change_value_combo(self.view.combo_model2, new_state)
        self.change_value_combo(self.view.combo_model3, new_state)
        self.change_value_combo(self.view.combo_better_model1, new_state)
        self.change_value_combo(self.view.combo_better_model2, new_state)
        self.change_value_combo(self.view.combo_better_model3, new_state)
        self.change_value_combo(self.view.best_model, new_state)

