import tkinter as tk
import os
import torch
import json
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import threading
import wave
import numpy as np
from vosk import Model, KaldiRecognizer, SpkModel, SetLogLevel

SetLogLevel(-1)

def cosine_dist(x, y):
    nx = np.array(x)
    ny = np.array(y)
    return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

def analyze():
    filename = file.get()
    prev_speaker = ''
    prev_speaker_text = ''
    model = Model("vosk-model-small-ru-0.22")
    spk_model = SpkModel("vosk-model-spk-0.4")
    try:
        wf = wave.open(filename, "rb")
    except BaseException as e:
        mb.showerror(title='Ошибка', message='Ошибка чтения файла')
        lb.configure(text='Ошибка. Попробуйте выбрать другой файл.')
        window.update_idletasks()
        return
    else:
        rcgn_fr = wf.getframerate() * wf.getnchannels()
        rec = KaldiRecognizer(model, rcgn_fr, spk_model)
        rec.SetSpkModel(spk_model)
        model, example_texts, languages, punct, apply_te = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                          model='silero_te')
        result = ''
        speakers = dict()
        last_n = False
        read_block_size = 4000
        wf.rewind()
        # read_block_size = wf.getnframes()
        i = 0
        j = 0
        while True:  # Можно читать файл блоками, тогда можно выводить распознанный текст частями, но слова на границе блоков могут быть распознаны некорректно
            if i%20 == 0:
                lb.configure(text='Загрузка' + '.'*(j%4))
                j = j + 1
                window.update_idletasks()
            data = wf.readframes(read_block_size)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                is_speaker = False
                if 'spk' in res:
                    spk = res['spk']
                    for speaker,vect in speakers.items():
                        if cosine_dist(vect, spk) < 0.85:
                            current_speaker = speaker
                            is_speaker = True
                            break
                    if not is_speaker:
                        current_speaker = f'Спикер {len(speakers)+1}'
                        speakers[current_speaker] = spk
                if res['text'] != '':
                    if not prev_speaker == current_speaker:
                        if prev_speaker_text:
                            new_res = apply_te(prev_speaker_text, lan='ru')
                            result += f"{prev_speaker}:\n{new_res}\n"
                        prev_speaker_text = res['text']
                    else:
                        prev_speaker_text += f"\n{res['text']}"
                    prev_speaker = current_speaker
                    last_n = False
                elif not last_n:
                    result += '\n'
                    last_n = True
            i = i + 1
        res = json.loads(rec.FinalResult())
        prev_speaker_text += f" {res['text']}"
        new_res = apply_te(prev_speaker_text, lan='ru')
        if prev_speaker_text:
            result += f"{prev_speaker}:\n{new_res}\n"
        lb.configure(text='Готово')
        txt.configure(state=tk.NORMAL)
        txt.delete(1.0, tk.END)
        txt.insert(1.0, result)
        txt.configure(state=tk.DISABLED)

def loading():
    lb.configure(text='Загрузка...')
    x = threading.Thread(target=analyze)
    x.start()

def select_file():
    filename = fd.askopenfilename(
        title='Открыть звуковой файл',
        initialdir=os.getcwd(),
        filetypes=[('Sound files ', '*.wav')])
    file.delete(0, tk.END)
    file.insert(0, filename)

def save_file():
    f = fd.asksaveasfile(
        title='Сохранить как',
        initialdir=os.getcwd(),
        filetypes=[('Text files', '*.txt')])
    text = txt.get(1.0, tk.END)
    f.write(text)
    f.close()

def show_info():
    mb.showinfo(title='О программе', \
                message='"Программа создана в рамках дисциплины Машинное обучение в инженерии"'
                        '\n©Чашкин Леонид Борисович, БИВ196')

def close_app():
    window.destroy()

window = tk.Tk()
window.title('Задание 2')
window.geometry('600x350')
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Сохранить текст', command=save_file)
filemenu.add_command(label='Выход', command=close_app)
menubar.add_cascade(menu=filemenu, label='Файл')
menubar.add_command(label='О программе', command=show_info)
window.config(menu=menubar)
lb = tk.Label(text='Имя файла (.wav)')
lb.grid(column=0, row=0)
file = tk.Entry(window,width=60)
file.grid(column=1, row=0)
btn_load = tk.Button(window, text='Открыть файл', command=select_file)
btn_load.grid(column=2, row=0)
btn_start = tk.Button(window, text='Преобразовать', command=loading)
btn_start.grid(column=0, row=1, columnspan=2)
lb = tk.Label(text='Выберите файл и нажмите "Преобразовать"')
lb.grid(column=0, row=2, columnspan=2)
txt = tk.Text(height=15, width=50, wrap=tk.WORD, state=tk.DISABLED)
txt.grid(column=0, row=3, columnspan=3)
sb = tk.Scrollbar(window, orient=tk.VERTICAL)
sb.grid(column=2, row=3, sticky='ns')
sb.config(command=txt.yview)
txt['yscrollcommand'] = sb.set
window.mainloop()
