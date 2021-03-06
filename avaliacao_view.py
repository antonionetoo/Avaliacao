from tkinter import Tk, Button, Label, Entry, Text, constants, IntVar, Radiobutton, Checkbutton
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

class TelaAvaliacao():
    def __init__(self, controller):
        self.window = Tk()
        self.controller = controller
        self.options_evaluate     = ['Correct', 'Incorrect', 'Partially correct']
        self.options_evaluate_compare = ['Better', 'Equal', 'Worse']
    
    def navegation(self):
        self.btn_previous = Button(self.window, text = 'Previous', command = self.controller.previous_example)
        self.btn_previous.grid(row = 21, column = 0)

        self.lb_referencia_deanon = Label(self.window, text = 'Example nº')
        self.lb_referencia_deanon.grid(row = 20, column = 1, sticky = constants.W)

        self.txt_num_exemplo = Entry(self.window, width = 10)
        self.txt_num_exemplo.grid(row = 21, column = 1, sticky = constants.W)
        self.txt_num_exemplo.bind('<Return>', self.controller.enter_instance_number)
        
        self.lb_identifier = Label(self.window, text = 'Identifier')
        self.lb_identifier.grid(row = 20, column = 2, sticky = constants.W)
        
        self.txt_identifier = Entry(self.window, width = 17)
        self.txt_identifier.grid(row = 21, column = 2, sticky = constants.W)
        self.txt_identifier.bind('<Return>', self.controller.enter_identifier)

        self.btn_next = Button(self.window, text = 'Next', command = self.controller.next_instance)
        self.btn_next.grid(row = 21, column = 3)
    
    def reference(self):
        self.lb_reference = Label(self.window, width = 50, text = 'NL reference')
        self.lb_reference.grid(row = 0, column = 4, columnspan = 2)

        self.txt_reference = Entry(self.window)
        self.txt_reference.grid(row = 1, column = 4, sticky = constants.W + constants.E, columnspan = 2)

        self.ignore = IntVar()
        self.check_ignore = Checkbutton(self.window, text = 'Ignore', offvalue = 0, onvalue = 1, variable = self.ignore, command = self.controller.ignore)
        self.check_ignore.grid(row = 1, column = 6, sticky = constants.W + constants.E)
    
    def baseline(self):
        self.lb_baseline = Label(self.window, width = 50, text = 'Baseline')
        self.lb_baseline.grid(row = 2, column = 4, columnspan = 2)

        self.txt_baseline = Entry(self.window)
        self.txt_baseline.grid(row = 3, column = 4, sticky = constants.W + constants.E, columnspan = 2)
        
        self.combo_baseline = ttk.Combobox(self.window, values = self.options_evaluate, state="readonly", width = 15)
        self.combo_baseline.grid(row = 3, column = 6)

    def model1(self):
        self.lb_model1 = Label(self.window, width = 50, text = 'Model 1')
        self.lb_model1.grid(row = 4, column = 4, columnspan = 2)

        self.txt_model1 = Entry(self.window)
        self.txt_model1.grid(row = 5, column = 4, sticky = constants.W + constants.E, columnspan = 2)
                
        self.combo_model1 = ttk.Combobox(self.window, values = self.options_evaluate, state="readonly", width = 15)
        self.combo_model1.grid(row = 5, column = 6)

        self.combo_better_model1 = ttk.Combobox(self.window, values = self.options_evaluate_compare, state="readonly", width = 10)
        self.combo_better_model1.grid(row = 5, column = 7)
        
    def model2(self):
        self.lb_model2 = Label(self.window, width = 50, text = 'Model 2')
        self.lb_model2.grid(row = 6, column = 4, columnspan = 2)

        self.txt_model2 = Entry(self.window)
        self.txt_model2.grid(row = 7, column = 4, sticky = constants.W + constants.E, columnspan = 2)
        
        self.combo_model2 = ttk.Combobox(self.window, values = self.options_evaluate, state="readonly", width = 15)
        self.combo_model2.grid(row = 7, column = 6)
        
        self.combo_better_model2 = ttk.Combobox(self.window, values = self.options_evaluate_compare, state="readonly", width = 10)
        self.combo_better_model2.grid(row = 7, column = 7)
    
    def model3(self):
        self.lb_model3 = Label(self.window, width = 50, text = 'Model 3')
        self.lb_model3.grid(row = 8, column = 4, columnspan = 2)

        self.txt_model3 = Entry(self.window)
        self.txt_model3.grid(row = 9, column = 4, sticky = constants.W + constants.E, columnspan = 2)
        
        self.combo_model3 = ttk.Combobox(self.window, values = self.options_evaluate, state="readonly", width = 15)
        self.combo_model3.grid(row = 9, column = 6)
        
        self.combo_better_model3 = ttk.Combobox(self.window, values = self.options_evaluate_compare, state="readonly", width = 10)
        self.combo_better_model3.grid(row = 9, column = 7)
        
    def options_better_model(self):    
        self.txt_choose_better_model = Label(self.window, text = 'Best Model:', width = 15)
        #self.choose_better_model.config(font=(None, 12))

        self.txt_choose_better_model.grid(row = 10, column = 4, columnspan = 2)
        
        self.best_model = ttk.Combobox(self.window, values = ['Nenhum', 'Modelo 1', 'Modelo 2', 'Modelo 3'], state="readonly", width = 15)
        self.best_model.grid(row = 10, column = 6, columnspan = 2, sticky = constants.W + constants.E)
        
        # self.best_model = IntVar()
        # self.best_model.set(0)
        
        # self.none_model = Radiobutton(self.window, text='Nenhum', variable = self.best_model, value = 0, width = 10)
        # self.none_model.grid(row = 10, column = 5)
        
        # self.option_model1 = Radiobutton(self.window, text='Modelo 1', variable = self.best_model, value = 1, width = 10)
        # self.option_model1.grid(row = 10, column = 6)

        # self.option_model2 = Radiobutton(self.window, text='Modelo 2', variable = self.best_model, value = 2, width = 10)
        # self.option_model2.grid(row = 10, column = 7)
        
    def observation(self):
        self.lb_predita_ln = Label(self.window, width = 50, text = 'Observation')
        self.lb_predita_ln.grid(row = 11, column = 4, columns = 2)
        
        self.txt_observacao = Text(self.window, height = 15)
        self.txt_observacao.grid(row = 12, column = 4, rowspan = 8, columnspan = 4, sticky = constants.W)

    def save_and_open_file(self):
        self.btn_salvar_arquivo = Button(self.window, text = 'Save file', command = self.controller.save_file)
        self.btn_salvar_arquivo.grid(row = 20, column = 4)

        self.btn_abrir_arquivo = Button(self.window, text = 'Open file', command = self.controller.file_open)
        self.btn_abrir_arquivo.grid(row = 20, column = 6, sticky = constants.W)
    
    def plot_image(self, fig):
        canvas = FigureCanvasTkAgg(fig, master = self.window)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 4, rowspan = 21, sticky = constants.W + constants.E)

    def on_closing(self):
        self.window.quit()
        self.window.destroy()

    def show_interface(self):
        self.navegation()
        self.reference()
        self.baseline()

        self.model1()
        self.model2()
        self.model3()
        self.options_better_model()
        
        self.observation()
        self.save_and_open_file()

        self.window.title("Evaluation interface")
        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)
        
        self.window.mainloop()