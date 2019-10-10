from tkinter import Tk, Button, Label, Entry, Text, constants
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

class TelaAvaliacao():
    def __init__(self, controller):
        self.window = Tk()
        self.controller = controller
        self.options_evaluate     = ['Correto', 'Incorreto', 'Parcialmente Correto']
        self.options_combo_ref_ln = ['Correto', 'Ignorar']
    
    def navegation(self):
        self.btn_previous = Button(self.window, text = 'Anterior', command = self.controller.previous_example)
        self.btn_previous.grid(row = 21, column = 0)

        self.lb_referencia_deanon = Label(self.window, text = 'Exemplo nº')
        self.lb_referencia_deanon.grid(row = 21, column = 1, sticky = constants.E)

        self.txt_num_exemplo = Entry(self.window, width = 10)
        self.txt_num_exemplo.grid(row = 21, column = 2, sticky = constants.W)
        self.txt_num_exemplo.bind('<Return>', self.controller.enter)

        self.btn_next = Button(self.window, text = 'Próximo', command = self.controller.next_instance)
        self.btn_next.grid(row = 21, column = 4)
    
    def reference(self):
        self.lb_referencia_ln = Label(self.window, width = 50, text = 'Referência LN')
        self.lb_referencia_ln.grid(row = 0, column = 5, columnspan = 2)

        self.txt_referencia_ln = Entry(self.window)
        self.txt_referencia_ln.grid(row = 1, column = 5, sticky = constants.W + constants.E, columnspan = 2)

        self.combo_referencia_ln = ttk.Combobox(self.window, values = self.options_combo_ref_ln, state="readonly")
        self.combo_referencia_ln.grid(row = 1, column = 7)
        self.combo_referencia_ln.bind("<<ComboboxSelected>>", self.controller.change_combo_ref_ln)

    def deanon(self):
        self.lb_referencia_deanon = Label(self.window, width = 50, text = 'Desanonimizada a partir da AMR de referência')
        self.lb_referencia_deanon.grid(row = 2, column = 5, columnspan = 2)

        self.txt_referencia_deanon = Entry(self.window)
        self.txt_referencia_deanon.grid(row = 3, column = 5, sticky = constants.W + constants.E, columnspan = 2)

        self.combo_referencia_deanon = ttk.Combobox(self.window, values=self.options_evaluate, state="readonly")
        self.combo_referencia_deanon.grid(row = 3, column = 7)
        self.combo_referencia_deanon.bind("<<ComboboxSelected>>", self.controller.change_combo_referencia_deanon)
    
    def predict(self):
        self.lb_predita_ln = Label(self.window, width = 50, text = 'Predita modelo transformada em LN')
        self.lb_predita_ln.grid(row = 4, column = 5, columnspan = 2)

        self.txt_predita_ln = Entry(self.window)
        self.txt_predita_ln.grid(row = 5, column = 5, sticky = constants.W + constants.E, columnspan = 2)

        self.combo_predita_ln = ttk.Combobox(self.window, values = self.options_evaluate, state="readonly")
        self.combo_predita_ln.grid(row = 5, column = 7)
        self.combo_predita_ln.bind("<<ComboboxSelected>>", self.controller.change_combo_predita_ln)

    def observation(self):
        self.lb_predita_ln = Label(self.window, width = 50, text = 'Observações')
        self.lb_predita_ln.grid(row = 6, column = 5, columns = 3)

        self.txt_observacao = Text(self.window, height = 15)
        self.txt_observacao.grid(row = 7, column = 5, columnspan = 3, rowspan = 10, sticky = constants.W)
    
    def model(self):
        self.lb_modelo = Label(self.window, text = 'Modelo')
        self.lb_modelo.grid(row = 17, column = 6, sticky = constants.E)

        self.txt_modelo = Entry(self.window, state = "readonly")
        self.txt_modelo.grid(row = 17, column = 7, sticky = constants.W)

    def save_and_open_file(self):
        self.btn_salvar_arquivo = Button(self.window, text = 'Salvar Arquivo', command = self.controller.save_file)
        self.btn_salvar_arquivo.grid(row = 17, column = 5)

        self.btn_abrir_arquivo = Button(self.window, text = 'Abrir Arquivo', command = self.controller.file_open)
        self.btn_abrir_arquivo.grid(row = 17, column = 6, sticky = constants.W)
    
    def plot_image(self, fig):
        canvas = FigureCanvasTkAgg(fig, master = self.window)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 5, rowspan = 20, sticky = constants.W + constants.E)

    def on_closing(self):
        self.window.quit()
        self.window.destroy()

    def show_interface(self):
        self.navegation()
        self.reference()
        self.deanon()
        self.predict()
        self.observation()
        self.model()
        self.save_and_open_file()

        self.window.title("Interface de avaliação")
        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)
        
        self.window.mainloop()