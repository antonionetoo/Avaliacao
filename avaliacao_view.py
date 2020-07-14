from tkinter import Tk, Button, Label, Entry, Text, constants, IntVar, Radiobutton, Checkbutton
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

class TelaAvaliacao():
    def __init__(self, controller):
        self.window = Tk()
        self.controller = controller
        self.options_evaluate     = ['Correto', 'Incorreto', 'Parc. Correto']
        self.options_evaluate_compare = ['Melhor', 'Igual', 'Pior']
    
    def navegation(self):
        self.btn_previous = Button(self.window, text = 'Anterior', command = self.controller.previous_example)
        self.btn_previous.grid(row = 23, column = 0)

        self.lb_referencia_deanon = Label(self.window, text = 'Exemplo nº')
        self.lb_referencia_deanon.grid(row = 22, column = 1, sticky = constants.W)

        self.txt_num_exemplo = Entry(self.window, width = 10)
        self.txt_num_exemplo.grid(row = 23, column = 1, sticky = constants.W)
        self.txt_num_exemplo.bind('<Return>', self.controller.enter_instance_number)
        
        self.lb_identifier = Label(self.window, text = 'Identificador')
        self.lb_identifier.grid(row = 22, column = 2, sticky = constants.W)
        
        self.txt_identifier = Entry(self.window, width = 17)
        self.txt_identifier.grid(row = 23, column = 2, sticky = constants.W)
        self.txt_identifier.bind('<Return>', self.controller.enter_identifier)

        self.btn_next = Button(self.window, text = 'Próximo', command = self.controller.next_instance)
        self.btn_next.grid(row = 23, column = 3)
       
    def model1(self):
        self.lb_model1 = Label(self.window, width = 50, text = 'Modelo 1')
        self.lb_model1.grid(row = 4, column = 4)

        self.txt_model1 = Entry(self.window)
        self.txt_model1.grid(row = 5, column = 4, sticky = constants.W + constants.E)
                
        self.combo_model1 = ttk.Combobox(self.window, values = self.options_evaluate, state="readonly", width = 15)
        self.combo_model1.grid(row = 5, column = 5)

    def model2(self):
        self.lb_model2 = Label(self.window, width = 50, text = 'Modelo 2')
        self.lb_model2.grid(row = 6, column = 4)

        self.txt_model2 = Entry(self.window)
        self.txt_model2.grid(row = 7, column = 4, sticky = constants.W + constants.E)
        
        self.combo_model2 = ttk.Combobox(self.window, values = self.options_evaluate, state="readonly", width = 15)
        self.combo_model2.grid(row = 7, column = 5)

    def model3(self):
        self.lb_model3 = Label(self.window, width = 50, text = 'Modelo 3')
        self.lb_model3.grid(row = 8, column = 4)

        self.txt_model3 = Entry(self.window)
        self.txt_model3.grid(row = 9, column = 4, sticky = constants.W + constants.E)
                
        self.combo_model3 = ttk.Combobox(self.window, values = self.options_evaluate, state="readonly", width = 15)
        self.combo_model3.grid(row = 9, column = 5)   
    
    def model4(self):
        self.lb_model4 = Label(self.window, width = 50, text = 'Modelo 4')
        self.lb_model4.grid(row = 10, column = 4)

        self.txt_model4 = Entry(self.window)
        self.txt_model4.grid(row = 11, column = 4, sticky = constants.W + constants.E)
                
        self.combo_model4 = ttk.Combobox(self.window, values = self.options_evaluate, state="readonly", width = 15)
        self.combo_model4.grid(row = 11, column = 5)
        
    def options_better_model(self):    
        self.txt_choose_better_model = Label(self.window, text = 'Melhor modelo:', width = 15)
        
        self.txt_choose_better_model.grid(row = 12, column = 4)
        
        self.best_model = ttk.Combobox(self.window, values = ['Nenhum', 'Modelo 1', 'Modelo 2', 'Modelo 3', 'Modelo 4'], state="readonly", width = 15)
        self.best_model.grid(row = 12, column = 5, sticky = constants.W + constants.E)
        
    def observation(self):
        self.lb_predita_ln = Label(self.window, width = 50, text = 'Observações')
        self.lb_predita_ln.grid(row = 13, column = 4, columns = 2)
        
        self.txt_observacao = Text(self.window, height = 15)
        self.txt_observacao.grid(row = 14, column = 4, rowspan = 8, columnspan = 4, sticky = constants.W)

    def save_and_open_file(self):
        self.btn_salvar_arquivo = Button(self.window, text = 'Salvar Arquivo', command = self.controller.save_file)
        self.btn_salvar_arquivo.grid(row = 22, column = 4)

        self.btn_abrir_arquivo = Button(self.window, text = 'Abrir Arquivo', command = self.controller.file_open)
        self.btn_abrir_arquivo.grid(row = 22, column = 5, sticky = constants.W)
    
    def plot_image(self, fig):
        canvas = FigureCanvasTkAgg(fig, master = self.window)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 4, rowspan = 22, sticky = constants.W + constants.E)

    def on_closing(self):
        self.window.quit()
        self.window.destroy()

    def show_interface(self):
        self.navegation()

        self.model1()
        self.model2()
        self.model3()
        self.model4()
        
        self.options_better_model()
        
        self.observation()
        self.save_and_open_file()

        self.window.title("Interface de avaliação")
        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)
        
        self.window.mainloop()