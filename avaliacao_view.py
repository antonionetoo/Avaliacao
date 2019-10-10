from tkinter import *

from tkinter import *
#from tkFileDialog import *

from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure
import skimage.io as io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from tkinter import ttk

class TelaAvaliacao():
    def __init__(self, controller):
        self.window = Tk()
        self.controller = controller
        self.options_evaluate     = ['Correto', 'Incorreto', 'Parcialmente Correto']
        self.options_combo_ref_ln = ['Correto', 'Ignorar']
    
    def navegacao(self):
        self.btn_previous = Button(self.window, text = 'Anterior', command = self.controller.previous_example)
        self.btn_previous.grid(row = 21, column = 0)

        self.lb_referencia_deanon = Label(self.window, text = 'Exemplo nº')
        self.lb_referencia_deanon.grid(row = 21, column = 1, sticky = E)

        self.txt_num_exemplo = Entry(self.window, width = 10)
        self.txt_num_exemplo.grid(row = 21, column = 2, sticky = W)
        self.txt_num_exemplo.bind('<Return>', self.controller.enter)

        self.btn_next = Button(self.window, text = 'Próximo', command = self.controller.next_instance)
        self.btn_next.grid(row = 21, column = 4)
    
    def referencia(self):
        self.lb_referencia_ln = Label(self.window, width = 50, text = 'Referência LN')
        self.lb_referencia_ln.grid(row = 0, column = 5, columnspan = 2)

        self.txt_referencia_ln = Entry(self.window)
        self.txt_referencia_ln.grid(row = 1, column = 5, sticky = W+E, columnspan = 2)

        self.combo_referencia_ln = ttk.Combobox(self.window, values = self.options_combo_ref_ln, state="readonly")
        self.combo_referencia_ln.grid(row = 1, column = 7)
        self.combo_referencia_ln.bind("<<ComboboxSelected>>", self.controller.change_combo_ref_ln)

    def deanon(self):
        self.lb_referencia_deanon = Label(self.window, width = 50, text = 'Desanonimizada a partir da AMR de referência')
        self.lb_referencia_deanon.grid(row = 2, column = 5, columnspan = 2)

        self.txt_referencia_deanon = Entry(self.window)
        self.txt_referencia_deanon.grid(row = 3, column = 5, sticky = W+E, columnspan = 2)

        self.combo_referencia_deanon = ttk.Combobox(self.window, values=self.options_evaluate, state="readonly")
        self.combo_referencia_deanon.grid(row = 3, column = 7)
        self.combo_referencia_deanon.bind("<<ComboboxSelected>>", self.controller.change_combo_referencia_deanon)
    
    def predita(self):
        self.lb_predita_ln = Label(self.window, width = 50, text = 'Predita modelo transformada em LN')
        self.lb_predita_ln.grid(row = 4, column = 5, columnspan = 2)

        self.txt_predita_ln = Entry(self.window)
        self.txt_predita_ln.grid(row = 5, column = 5, sticky = W+E, columnspan = 2)

        self.combo_predita_ln = ttk.Combobox(self.window, values = self.options_evaluate, state="readonly")
        self.combo_predita_ln.grid(row = 5, column = 7)
        self.combo_predita_ln.bind("<<ComboboxSelected>>", self.controller.change_combo_predita_ln)

    def observacao(self):
        self.lb_predita_ln = Label(self.window, width = 50, text = 'Observações')
        self.lb_predita_ln.grid(row = 6, column = 5, columns = 3)

        self.txt_observacao = Text(self.window, height = 15)
        self.txt_observacao.grid(row = 7, column = 5, columnspan = 3, rowspan = 10, sticky = W)
    
    def modelo(self):
        self.lb_modelo = Label(self.window, text = 'Modelo')
        self.lb_modelo.grid(row = 17, column = 6, sticky = E)

        self.txt_modelo = Entry(self.window, state = "readonly")
        self.txt_modelo.grid(row = 17, column = 7, sticky = W)

    def salvar_abrir_arquivo(self):
        self.btn_salvar_arquivo = Button(self.window, text = 'Salvar Arquivo', command = self.controller.save_file)
        self.btn_salvar_arquivo.grid(row = 17, column = 5)

        self.btn_abrir_arquivo = Button(self.window, text = 'Abrir Arquivo', command = self.controller.file_open)
        self.btn_abrir_arquivo.grid(row = 17, column = 6, sticky = W)
    
    def draw_bbox(ax, bbox, edge_color='red', line_width =3):
        bbox_plot = mpatches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3],
            fill = False, edgecolor = edge_color, linewidth = line_width)
        ax.add_patch(bbox_plot)
    
    def on_closing(self):
        self.window.quit()
        self.window.destroy()

    def exibi_interface(self):
        self.navegacao()
        self.referencia()
        self.deanon()
        self.predita()
        self.observacao()
        self.modelo()
        self.salvar_abrir_arquivo()

        self.window.title("Interface de avaliação")
        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)
        
        self.window.mainloop()