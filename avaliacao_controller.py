from avaliacao_model import AvaliacaoModel
from avaliacao_view import TelaAvaliacao

from tkinter import constants
from tkinter import filedialog
from tkinter import messagebox

class ControllerAvalicao():

    def __init__(self):
        self.model = AvaliacaoModel()
        self.view = TelaAvaliacao(self)

    def enter_instance_number(self, event):
        self.model.save_observation(self.view.txt_observacao.get("1.0", constants.END))
        
        try:
            n_instance = int(self.view.txt_num_exemplo.get())
            self.model.go_to_instance(n_instance)
        except:
            messagebox.showinfo("Erro", "Exemplo não encontrado")
            self.load_phrase(self.view.txt_num_exemplo, self.model.index)
            return

        self.load_informations()
    
    def enter_identifier(self, event):
        key = self.view.txt_identifier.get()
        
        try:
            self.save_informations()
            self.model.go_to_key(key)
            
            self.load_informations()
        except:
            messagebox.showinfo("Erro", "Exemplo não encontrado")

    def save_file(self):
        dir_split = self.model.dir_file.split('/')
        
        f = filedialog.asksaveasfile(mode='w', initialdir = '/'.join(dir_split[0:len(dir_split) - 1]), 
               initialfile = dir_split[-1], defaultextension = '.json')        

        if f is None:
            return

        self.save_informations()
        self.model.save_json(self.model.data, f)

    def file_open(self):
        mask = [("Arquivos json","*.json")]
        f = filedialog.askopenfile(filetypes=mask, mode='r')

        if f == None:
            return 
        
        data = self.model.load_json(f)        
        
        """
        self.view.txt_modelo.configure(state = constants.NORMAL)
        self.view.txt_modelo.delete(0, constants.END)
        self.view.txt_modelo.insert(0, file['model'])

        self.view.txt_modelo.configure(state = 'readonly')
        """

        self.model.build_number_to_positions(data)
        self.load_informations()
    
    def save_informations(self):
        model1      = self.view.better_model1.get()
        model2      = self.view.better_model2.get()
        best_model  = self.view.best_model.get()
        observation = self.view.txt_observacao.get("1.0", constants.END)
        
        self.model.save_informations(model1, model2, best_model, observation)
    
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
        
        #try:
        self.view.txt_observacao.delete(1.0, constants.END)
        self.view.txt_observacao.insert(constants.END, observation)
        
        self.view.model1 = model1
        #model1, model2, best_model
        #except KeyError:
        #    self.view.txt_observacao.insert(constants.END, '')
        
        #self.load_phrase(self.view.txt_baseline, baseline)

        #self.load_phrase(self.view.txt_model1, predicted_model1)
        #self.load_phrase(self.view.txt_model1, predicted_model1)
        #self.load_phrase(self.view.txt_model1, predicted_model1)

        """
        self.load_phrase(self.view.txt_referencia_ln, ln_ref)
        self.load_phrase(self.view.txt_referencia_deanon, ln_ref_anon)
        self.load_phrase(self.view.txt_predita_ln, ln_pred)

        self.view.txt_observacao.delete(1.0, constants.END)
        try:
            self.view.txt_observacao.insert(constants.END, ln_observacao)
        except KeyError:
            self.view.txt_observacao.insert(constants.END, '')
        """

    def load_informations(self):
        self.view.plot_image(self.model.load_image())

        self.load_phrases()
        self.load_phrase(self.view.txt_num_exemplo, self.model.index)
        
    def previous_example(self):
        self.save_informations()
        self.save_informations()
        self.model.previous_example()

        self.load_informations()
    
    def next_instance(self):
        self.save_informations()
        self.save_informations()
        self.model.next_instance()

        self.load_informations()

    def start(self):
        self.view.show_interface()
        
if __name__ == '__main__':
    controller = ControllerAvalicao()
    controller.start()