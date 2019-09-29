from tkinter import *

from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure
import skimage.io as io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from helpjson import *
from tkinter import ttk

options_evaluate = ['Correto', 'Incorreto', 'Parcialmente Correto']
data = None
global i, j
i = 0
j = -1

def next():
    global i, j
    j+=1
    if j > len(data[i]['regions']) - 1:
        i+=1
        j = 0

    load_information(data[i]['regions'][j])

def previous():
    global i, j
    j-=1
    if j < 0:
        i-=1
        j = len(data[i]['regions']) - 1
    
    load_information(data[i]['regions'][j])

def load_json(name_data):
    return get_json(name_data)

def draw_bbox(ax, bbox, edge_color='red', line_width=3):
  bbox_plot = mpatches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3],
      fill=False, edgecolor=edge_color, linewidth=line_width)
  ax.add_patch(bbox_plot)

def load_image(region):
    bbox = [region['x'], region['y'], region['width'], region['height']]
    path_image = 'images_id/{}.jpg'.format(region['image_id'])

    img = io.imread(path_image)
    fig = plt.figure()
    plt.cla()
    plt.imshow(img)

    ax = plt.gca()
    draw_bbox(ax, bbox)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 5, rowspan = 20, sticky = W+E)

def load_phrase(txt, region, key):
    txt.delete(0, END)
    txt.insert(0, region['phrase']['ln'][key])

def load_phrases(region):
    load_phrase(txt_referencia_ln, region, 'ln_ref')
    load_phrase(txt_referencia_deanon, region, 'ln_ref_anon')
    load_phrase(txt_predita_ln, region, 'ln_pred')

def load_combo(key, combo):
    global i, j
    if key in data[i]['regions'][j]['phrase']['ln']:
        option = [k for k, v in enumerate(options_evaluate) if v == data[i]['regions'][j]['phrase']['ln'][key]]
        if len(option) == 0 :
            data[i]['regions'][j]['phrase']['ln'][key] = None
        else:
            combo.current(option[0])
    else:
        combo.set('')

def load_combos(region):
    #load_combo('ln_ref_eval', combo_referencia_ln)
    load_combo('ln_ref_anon_eval', combo_referencia_deanon)
    load_combo('ln_pred_eval', combo_predita_ln)

def load_information(region):
    load_image(region)
    load_phrases(region)
    load_combos(region)
    
def change_combo_ref_ln(event):
    data[i]['regions'][j]['phrase']['ln']['ln_ref_eval'] = combo_referencia_ln.get()    

def change_combo_referencia_deanon(event):
    data[i]['regions'][j]['phrase']['ln']['ln_ref_anon_eval'] = combo_referencia_deanon.get()    

def change_combo_predita_ln(event):
    data[i]['regions'][j]['phrase']['ln']['ln_pred_eval'] = combo_predita_ln.get()    

window = Tk()

btn_previous = Button(window, text = 'Anterior', command = previous)
btn_previous.grid(row = 21, column = 0)

btn_next = Button(window, text = 'Próximo', command = next)
btn_next.grid(row = 21, column = 4)

lb_referencia_ln = Label(window, width = 50, text = 'Referência LN')
lb_referencia_ln.grid(row = 0, column = 5)

txt_referencia_ln = Entry(window)
txt_referencia_ln.grid(row = 1, column = 5, sticky = W+E)
"""
combo_referencia_ln = ttk.Combobox(window, values=options_evaluate, state="readonly")
combo_referencia_ln.grid(row = 1, column = 6)
combo_referencia_ln.bind("<<ComboboxSelected>>", change_combo_ref_ln)
"""

lb_referencia_deanon = Label(window, width = 50, text = 'Desanonimzada a partir da AMR de referência')
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


def on_closing():
  window.quit()
  window.destroy()
  save_json('data_eval.json', data)

window.protocol('WM_DELETE_WINDOW', on_closing)

data = load_json('data_eval.json')
next()

window.mainloop()

"""
from helpjson import *
data = get_json('data_small.json')
data2 = []
for d in data:
    for region in d['regions']:
        if region['phrase']['ln']['ln_pred']:
            data2.append(d)
            break

save_json('data_eval.json', data2)
"""