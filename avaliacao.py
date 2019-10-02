from tkinter import *
from tkFileDialog import *

from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure
import skimage.io as io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from helpjson import *
from tkinter import ttk

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
    index += 1

    load_information()

def previous_example():
    save_observation()

    global index
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

    #load_phrase(text_observacao, region, 'ln_observacao')
    text_observacao.delete(1.0, END)
    try:
        text_observacao.insert(END, region['phrase']['ln']['ln_observacao'])
    except KeyError:
        text_observacao.insert(END, '')

def load_combo(key, region, combo, values, default = ''):
    if key in region:
        option = [k for k, v in enumerate(values) if v == region['phrase']['ln'][key]]
        if len(option) == 0 :
            region['phrase']['ln'][key] = None
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
    global index
    index = n_instance

    load_information()

def build_number_to_positions():
    k = -1
    for i, d in enumerate(data):
        for j, r in enumerate(d['regions']):
            k += 1
            number_to_positions[k] = [i, j]

def save():
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = str(text.get(1.0, END)) # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close() # `()` was missing.

window = Tk()

btn_previous = Button(window, text = 'Anterior', command = previous_example)
btn_previous.grid(row = 21, column = 0)

btn_next = Button(window, text = 'Próximo', command = next_instance)
btn_next.grid(row = 21, column = 4)

lb_referencia_ln = Label(window, width = 50, text = 'Referência LN')
lb_referencia_ln.grid(row = 0, column = 5)

txt_referencia_ln = Entry(window)
txt_referencia_ln.grid(row = 1, column = 5, sticky = W+E)

combo_referencia_ln = ttk.Combobox(window, values = options_combo_ref_ln, state="readonly")
combo_referencia_ln.grid(row = 1, column = 6)
combo_referencia_ln.bind("<<ComboboxSelected>>", change_combo_ref_ln)

lb_referencia_deanon = Label(window, width = 50, text = 'Desanonimizada a partir da AMR de referência')
lb_referencia_deanon.grid(row = 2, column = 5)

txt_referencia_deanon = Entry(window)
txt_referencia_deanon.grid(row = 3, column = 5, sticky = W+E)

combo_referencia_deanon = ttk.Combobox(window, values=options_evaluate, state="readonly")
combo_referencia_deanon.grid(row = 3, column = 6)
combo_referencia_deanon.bind("<<ComboboxSelected>>", change_combo_referencia_deanon)

lb_predita_ln = Label(window, width = 50, text = 'Predita modelo transformada em LN')
lb_predita_ln.grid(row = 4, column = 5)

txt_predita_ln = Entry(window)
txt_predita_ln.grid(row = 5, column = 5, sticky = W+E)

combo_predita_ln = ttk.Combobox(window, values=options_evaluate, state="readonly")
combo_predita_ln.grid(row = 5, column = 6)
combo_predita_ln.bind("<<ComboboxSelected>>", change_combo_predita_ln)

lb_predita_ln = Label(window, width = 50, text = 'Observações')
lb_predita_ln.grid(row = 6, column = 5, columns = 2)

text_observacao = Text(window, height = 15)
text_observacao.grid(row = 7, column = 5, columnspan = 2, rowspan = 10, sticky = W+E)

lb_referencia_deanon = Label(window, width = 50, text = 'Exemplo nº')
lb_referencia_deanon.grid(row = 17, column = 5, sticky = E)

txt_num_exemplo = Entry(window)
txt_num_exemplo.grid(row = 17, column = 6)
txt_num_exemplo.bind('<Return>', enter)

btn_previous = Button(window, text = 'Salvar', command = save)
btn_previous.grid(row = 18, column = 5)

def on_closing():
  window.quit()
  window.destroy()
  save_json('data_eval.json', data)

window.protocol('WM_DELETE_WINDOW', on_closing)

data = load_json('data_eval.json')
build_number_to_positions()

load_information()

window.mainloop()
