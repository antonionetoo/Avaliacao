from avaliacao_model import AvaliacaoModel
from avaliacao_view import TelaAvaliacao

from tkinter import filedialog
from tkinter import *
from helpjson import *

class ControllerAvalicao():

    def __init__(self):
        self.model = AvaliacaoModel()
        self.view = TelaAvaliacao(self)
    
    def change_combo_ref_ln(self, event):
        value = self.view.combo_referencia_ln.get()

        region = model.curret_region()
        region['phrase']['ln']['ln_ref_eval'] = value

        if value == 'Ignorar':
            self.view.combo_predita_ln.config(state=DISABLED)
            self.view.combo_referencia_deanon.config(state=DISABLED)

            self.view.combo_referencia_deanon.set('')
            self.change_combo_referencia_deanon(None)

            self.view.combo_predita_ln.set('')
            self.change_combo_predita_ln(None)
        else:
            self.view.combo_predita_ln.config(state='readonly')
            self.view.combo_referencia_deanon.config(state='readonly')
    
    def change_combo_referencia_deanon(self, event):
        region = self.model.curret_region()
        region['phrase']['ln']['ln_ref_anon_eval'] = combo_referencia_deanon.get()    

    def change_combo_predita_ln(self, event):
        region = self.model.curret_region()
        region['phrase']['ln']['ln_pred_eval'] = combo_predita_ln.get()    

    def enter(self, event):
        save_observation()

        n_instance = int(txt_num_exemplo.get())

        try:
            number_to_positions[n_instance]
        except KeyError:
            messagebox.showinfo("Erro", "Exemplo não encontrado")
            return

        global index
        index = n_instance

        load_information()

    def save_file(self):
        global dir_file
        dir_split = dir_file.split('/')

        f = filedialog.asksaveasfile(mode='w', initialdir = '/'.join(dir_split[0:len(dir_split) - 1]), 
                initialfile = dir_split[-1], defaultextension = '.json')
        if f is None:
            return

        save_observation()
        global data
        new_data = {'data': data, 'model': txt_modelo.get()}
        json.dump(new_data, f)
        f.close()

    def file_open(self):
        mask = [("Arquivos json","*.json")]
        f = filedialog.askopenfile(filetypes=mask, mode='r')

        if f == None:
            return 
        
        global data
        file = json.load(f)

        global dir_file
        dir_file = f.name

        f.close()
        
        self.view.txt_modelo.configure(state = NORMAL)

        self.view.txt_modelo.delete(0, END)
        self.view.txt_modelo.insert(0, file['model'])

        self.view.txt_modelo.configure(state = 'readonly')

        data = file['data']
        self.model.build_number_to_positions(data)
        ln_ref, ln_ref_anon, ln_pred, ln_pred, ln_observacao, ln_ref_eval, ln_ref_anon_eval, ln_pred_eval, index = self.model.load_information()
    
    def start(self):
        self.view.exibi_interface()
    
    def previous_example(self):
        value = self.view.text_observacao.get("1.0", END)
        self.model.save_observation(value)

        self.model.previous_example()
    
    def next_instance(self):
        save_observation()

        global index 
        if index < len(number_to_positions) - 1:
            index += 1    
            load_information()

if __name__ == '__main__':
    controller = ControllerAvalicao()
    controller.start()
