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


if __name__ == "__main__":
    window = tk.Tk()
    Program(window)