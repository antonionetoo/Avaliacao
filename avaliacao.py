from tkinter import *
#from tkFileDialog import *
from tkinter import filedialog

from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure
import skimage.io as io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from helpjson import *
from tkinter import ttk
from tkinter import messagebox

options_evaluate     = ['Correto', 'Incorreto', 'Parcialmente Correto']
options_combo_ref_ln = ['Correto', 'Ignorar']
data = None
number_to_positions = dict()

global index
index = 0

def save_observation():
    region = curret_region()
    region['phrase']['ln']['ln_observacao'] = text_observacao.get("1.0", END)

def next_instance():
    save_observation()

    global index 
    if index < len(number_to_positions) - 1:
        index += 1    
        load_information()

def previous_example():
    save_observation()

    global index
    if index > 0:
        index -= 1
        load_information()

def curret_region():
    i = number_to_positions[index][0]
    j = number_to_positions[index][1]

    return data[i]['regions'][j]

def load_json(name_data):
    return get_json(name_data)

def draw_bbox(ax, bbox, edge_color='red', line_width =3):
  bbox_plot = mpatches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3],
      fill = False, edgecolor = edge_color, linewidth = line_width)
  ax.add_patch(bbox_plot)

def load_image(region):
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

def load_phrase(txt, region, key):
    txt.delete(0, END)
    txt.insert(0, region['phrase']['ln'][key])

def load_phrases(region):
    load_phrase(txt_referencia_ln, region, 'ln_ref')
    load_phrase(txt_referencia_deanon, region, 'ln_ref_anon')
    load_phrase(txt_predita_ln, region, 'ln_pred')

    text_observacao.delete(1.0, END)
    try:
        text_observacao.insert(END, region['phrase']['ln']['ln_observacao'])
    except KeyError:
        text_observacao.insert(END, '')

def load_combo(key, region, combo, values, default = ''):
    if key in region['phrase']['ln']:
        option = [k for k, v in enumerate(values) if v == region['phrase']['ln'][key]]
        if len(option) == 0 :
            region['phrase']['ln'][key] = None
            combo.set(default)
        else:
            combo.current(option[0])
    else:
        combo.set(default)

def load_combos(region):
    load_combo('ln_ref_eval', region, combo_referencia_ln, options_combo_ref_ln, 'Correto')
    load_combo('ln_ref_anon_eval', region, combo_referencia_deanon, options_evaluate)
    load_combo('ln_pred_eval', region, combo_predita_ln, options_evaluate)

def load_information():
    region = curret_region()

    load_image(region)
    load_phrases(region)
    load_combos(region)

    txt_num_exemplo.delete(0, END)
    txt_num_exemplo.insert(0, index)
    
def change_combo_ref_ln(event):
    value = combo_referencia_ln.get()

    region = curret_region()
    region['phrase']['ln']['ln_ref_eval'] = value

    if value == 'Ignorar':
        combo_predita_ln.config(state=DISABLED)
        combo_referencia_deanon.config(state=DISABLED)

        combo_referencia_deanon.set('')
        change_combo_referencia_deanon(None)

        combo_predita_ln.set('')
        change_combo_predita_ln(None)
    else:
        combo_predita_ln.config(state='readonly')
        combo_referencia_deanon.config(state='readonly')
    
def change_combo_referencia_deanon(event):
    region = curret_region()
    region['phrase']['ln']['ln_ref_anon_eval'] = combo_referencia_deanon.get()    

def change_combo_predita_ln(event):
    region = curret_region()
    region['phrase']['ln']['ln_pred_eval'] = combo_predita_ln.get()    

def enter(event):
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

def build_number_to_positions(data):
    k = -1
    for i, d in enumerate(data):
        for j, _ in enumerate(d['regions']):
            k += 1
            number_to_positions[k] = [i, j]
    
    global index
    index = 0

def save_file():
    f = filedialog.asksaveasfile(mode='w', defaultextension=".json")
    if f is None:
        return

    save_observation()
    global data
    new_data = {'data': data, 'model': txt_modelo.get()}
    json.dump(new_data, f)
    f.close()

def file_open():
    mask = [("Arquivos json","*.json")]
    f = filedialog.askopenfile(filetypes=mask, mode='r')

    if f == None:
        return 
    
    global data
    file = json.load(f)
    f.close()

    txt_modelo.configure(state = NORMAL)

    txt_modelo.delete(0, END)
    txt_modelo.insert(0, file['model'])

    txt_modelo.configure(state = 'readonly')

    data = file['data']
    build_number_to_positions(data)
    load_information()
    
window = Tk()

btn_previous = Button(window, text = 'Anterior', command = previous_example)
btn_previous.grid(row = 21, column = 0)

lb_referencia_deanon = Label(window, text = 'Exemplo nº')
lb_referencia_deanon.grid(row = 21, column = 1, sticky = E)

txt_num_exemplo = Entry(window, width = 10)
txt_num_exemplo.grid(row = 21, column = 2, sticky = W)
txt_num_exemplo.bind('<Return>', enter)

btn_next = Button(window, text = 'Próximo', command = next_instance)
btn_next.grid(row = 21, column = 4)

lb_referencia_ln = Label(window, width = 50, text = 'Referência LN')
lb_referencia_ln.grid(row = 0, column = 5, columnspan = 2)

txt_referencia_ln = Entry(window)
txt_referencia_ln.grid(row = 1, column = 5, sticky = W+E, columnspan = 2)

combo_referencia_ln = ttk.Combobox(window, values = options_combo_ref_ln, state="readonly")
combo_referencia_ln.grid(row = 1, column = 7)
combo_referencia_ln.bind("<<ComboboxSelected>>", change_combo_ref_ln)

lb_referencia_deanon = Label(window, width = 50, text = 'Desanonimizada a partir da AMR de referência')
lb_referencia_deanon.grid(row = 2, column = 5, columnspan = 2)

txt_referencia_deanon = Entry(window)
txt_referencia_deanon.grid(row = 3, column = 5, sticky = W+E, columnspan = 2)

combo_referencia_deanon = ttk.Combobox(window, values=options_evaluate, state="readonly")
combo_referencia_deanon.grid(row = 3, column = 7)
combo_referencia_deanon.bind("<<ComboboxSelected>>", change_combo_referencia_deanon)

lb_predita_ln = Label(window, width = 50, text = 'Predita modelo transformada em LN')
lb_predita_ln.grid(row = 4, column = 5, columnspan = 2)

txt_predita_ln = Entry(window)
txt_predita_ln.grid(row = 5, column = 5, sticky = W+E, columnspan = 2)

combo_predita_ln = ttk.Combobox(window, values=options_evaluate, state="readonly")
combo_predita_ln.grid(row = 5, column = 7)
combo_predita_ln.bind("<<ComboboxSelected>>", change_combo_predita_ln)

lb_predita_ln = Label(window, width = 50, text = 'Observações')
lb_predita_ln.grid(row = 6, column = 5, columns = 3)

text_observacao = Text(window, height = 15)
text_observacao.grid(row = 7, column = 5, columnspan = 3, rowspan = 10, sticky = W)

lb_modelo = Label(window, text = 'Modelo')
lb_modelo.grid(row = 17, column = 6, sticky = E)

txt_modelo = Entry(window, state = "readonly")
txt_modelo.grid(row = 17, column = 7, sticky = W)

btn_previous = Button(window, text = 'Salvar Arquivo', command = save_file)
btn_previous.grid(row = 17, column = 5)

btn_previous = Button(window, text = 'Abrir Arquivo', command = file_open)
btn_previous.grid(row = 17, column = 6, sticky = W)

def on_closing():
  window.quit()
  window.destroy()

window.title("Interface de avaliação")
window.protocol('WM_DELETE_WINDOW', on_closing)

window.mainloop()