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

"""
Система представляет собой программный комплекс и предназначена для распознавания речи с аудиоматериала,
определения спикеров и расстановки знаков препинания.
Программное обеспечение представляет собой сочетание программной части и графического интерфейса.
Программа может быть использована для распознавания голосовых сообщений пользователей социальных сетей,
расшифровки аудиоматериалов конференций/собраний/лекций/публичных выступлений и создания субтитров.

"""

class Program():
    """
    Программа для перевода аудио файла в текст

    Класс предоставляет набор функций и графический интерфейс для реализации программы по транскрибации,
    диаризации и расстановки знаков препинания в тексте из аудио файла в формате wav и сохранения его в txt.

    :param window: Окно приложения
    :param menubar: Меню бар приложения
    :param filemenu: Меню файлв
    :param lb: Метка
    :param file: Поле ввода пути файла
    :param btn_load: Кнопка загрузки
    :param btn_start: Кнопка старта
    :param txt: Поле вывода текста
    :param sb: Метка
    """

    def __init__(self, window):
        self.window = window
        self.window.title('TPRO-project')
        self.window.geometry('600x350')
        self.menubar = tk.Menu(self.window)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Сохранить текст', command=self.save_file)
        self.filemenu.add_command(label='Выход', command=self.close_app)
        self.menubar.add_cascade(menu=self.filemenu, label='Файл')
        self.menubar.add_command(label='О программе', command=self.show_info)
        self.window.config(menu=self.menubar)
        self.lb = tk.Label(text='Имя файла (.wav)')
        self.lb.grid(column=0, row=0)
        self.file = tk.Entry(self.window, width=60)
        self.file.grid(column=1, row=0)
        self.btn_load = tk.Button(self.window, text='Открыть файл', command=self.select_file)
        self.btn_load.grid(column=2, row=0)
        self.btn_start = tk.Button(self.window, text='Преобразовать', command=self.loading)
        self.btn_start.grid(column=0, row=1, columnspan=2)
        self.lb = tk.Label(text='Выберите файл и нажмите "Преобразовать"')
        self.lb.grid(column=0, row=2, columnspan=2)
        self.txt = tk.Text(height=15, width=50, wrap=tk.WORD, state=tk.DISABLED)
        self.txt.grid(column=0, row=3, columnspan=3)
        self.sb = tk.Scrollbar(window, orient=tk.VERTICAL)
        self.sb.grid(column=2, row=3, sticky='ns')
        self.sb.config(command=self.txt.yview)
        self.txt['yscrollcommand'] = self.sb.set
        self.window.mainloop()

    def save_file(self):
        """
        Функция сохранения файла в формате *.txt
        """
        f = fd.asksaveasfile(
            title='Сохранить как',
            initialdir=os.getcwd(),
            filetypes=[('Text files', '*.txt')])
        text = self.txt.get(1.0, tk.END)
        f.write(text)
        f.close()

    def show_info(self):
        """
        Функция выводящая сведения 'О программе'
        """
        mb.showinfo(title='О программе', \
                    message='"Программа создана в рамках дисциплины ТПРО"'
                            '\n©Чашкин, Падалица, Маршутина, Степченко')

    def analyze(self):
        """
        Функция производящая анализ аудио файла

        Функция используя две vosk model small для получения текста из аудио файла и
        vosk model spk для разбиения по спикерам. Текст распознается только на русском языке.
        Функция может вернуть ошибку если файл не может быть прочитан.
        Успешным результатом работы функции является трансерибированный текст, который будет выведен в свойство txt
        :return:
        """
        filename = self.file.get()
        prev_speaker = ''
        prev_speaker_text = ''
        model = Model("vosk-model-small-ru-0.22")
        spk_model = SpkModel("vosk-model-spk-0.4")
        try:
            wf = wave.open(filename, "rb")
        except BaseException as e:
            mb.showerror(title='Ошибка', message='Ошибка чтения файла')
            self.lb.configure(text='Ошибка. Попробуйте выбрать другой файл.')
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
                if i % 20 == 0:
                    self.lb.configure(text='Загрузка' + '.' * (j % 4))
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
                        for speaker, vect in speakers.items():
                            if self.cosine_dist(vect, spk) < 0.85:
                                current_speaker = speaker
                                is_speaker = True
                                break
                        if not is_speaker:
                            current_speaker = f'Спикер {len(speakers) + 1}'
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
            self.lb.configure(text='Готово')
            self.txt.configure(state=tk.NORMAL)
            self.txt.delete(1.0, tk.END)
            self.txt.insert(1.0, result)
            self.txt.configure(state=tk.DISABLED)

if __name__ == "__main__":
    window = tk.Tk()
    Program(window)