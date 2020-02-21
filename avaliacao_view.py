from tkinter import Tk, Button, Label, Entry, Text, constants
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

class TelaAvaliacao():
    def __init__(self, controller):
        self.window = Tk()
        self.controller = controller
        self.options_evaluate     = ['Correto', 'Incorreto', 'Parcialmente Correto']
    
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
        self.lb_reference = Label(self.window, width = 50, text = 'Referência LN')
        self.lb_reference.grid(row = 0, column = 5, columnspan = 2)

        self.txt_reference = Entry(self.window)
        self.txt_reference.grid(row = 1, column = 5, sticky = constants.W + constants.E, columnspan = 2)
    
    def baseline(self):
        self.lb_baseline = Label(self.window, width = 50, text = 'Baseline')
        self.lb_baseline.grid(row = 2, column = 5, columnspan = 2)

        self.txt_baseline = Entry(self.window)
        self.txt_baseline.grid(row = 3, column = 5, sticky = constants.W + constants.E, columnspan = 2)

    def model1(self):
        self.lb_model1 = Label(self.window, width = 50, text = 'Modelo 1 (anon-1kk)')
        self.lb_model1.grid(row = 4, column = 5, columnspan = 2)

        self.txt_model1 = Entry(self.window)
        self.txt_model1.grid(row = 5, column = 5, sticky = constants.W + constants.E, columnspan = 2)

        self.check_model1 = ttk.Checkbutton(self.window, text = "Melhor que o baseline")
        self.check_model1.grid(row = 5, column = 7)

    def model2(self):
        self.lb_model2 = Label(self.window, width = 50, text = 'Modelo 2 (anonc-1kk)')
        self.lb_model2.grid(row = 6, column = 5, columnspan = 2)

        self.txt_model2 = Entry(self.window)
        self.txt_model2.grid(row = 7, column = 5, sticky = constants.W + constants.E, columnspan = 2)

        self.check_model2 = ttk.Checkbutton(self.window, text = "Melhor que o baseline")
        self.check_model2.grid(row = 7, column = 7)        
    
    def choose_better_model(self):
        self.choose_better_model = Label(self.window, text = 'Melhor modelo:')
        self.choose_better_model.config(font=(None, 12))

        self.choose_better_model.grid(row = 8, column = 5)

        option_model1 = ttk.Radiobutton(self.window, text="Modelo 1", value=1)
        option_model1.grid(row = 8, column = 6)

        option_model2 = ttk.Radiobutton(self.window, text="Modelo 2", value=2)
        option_model2.grid(row = 8, column = 7)
        
    def observation(self):
        self.lb_predita_ln = Label(self.window, width = 50, text = 'Observações')
        self.lb_predita_ln.grid(row = 9, column = 5, columns = 3)

        self.txt_observacao = Text(self.window, height = 15)
        self.txt_observacao.grid(row = 10, column = 5, columnspan = 3, rowspan = 10, sticky = constants.W)

    def save_and_open_file(self):
        self.btn_salvar_arquivo = Button(self.window, text = 'Salvar Arquivo', command = self.controller.save_file)
        self.btn_salvar_arquivo.grid(row = 20, column = 5)

        self.btn_abrir_arquivo = Button(self.window, text = 'Abrir Arquivo', command = self.controller.file_open)
        self.btn_abrir_arquivo.grid(row = 20, column = 6, sticky = constants.W)
    
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
        self.baseline()

        self.model1()
        self.model2()
        self.choose_better_model()
        
        self.observation()
        self.save_and_open_file()

        self.window.title("Interface de avaliação")
        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)
        
        self.window.mainloop()