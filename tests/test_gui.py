import os
import pytest
import tkinter as tk
from unittest.mock import patch, mock_open

from program.main import Program

@pytest.fixture
def program():
    root = tk.Tk()
    program = Program(root)
    root.withdraw()
    yield program
    root.destroy()


def test_initial_elements(program):
    assert program.window is not None
    assert program.menubar is not None
    assert program.filemenu is not None
    assert program.lb is not None
    assert program.file is not None
    assert program.btn_load is not None
    assert program.btn_start is not None
    assert program.txt is not None
    assert program.sb is not None


@patch("tkinter.filedialog.askopenfilename")
def test_select_file(mock_askopenfilename, program):
    expected_file_path = "test/test.wav"
    mock_askopenfilename.return_value = expected_file_path
    program.select_file()
    assert program.file.get() == expected_file_path


@patch("tkinter.filedialog.asksaveasfile", new_callable=mock_open)
def test_save_file(mock_asksaveasfile, program):
    expected_content = "Test content"

    program.txt.configure(state=tk.NORMAL)
    program.txt.insert("1.0", expected_content)
    program.save_file()

    mock_asksaveasfile.assert_called_once_with(
        title="Сохранить как",
        initialdir=os.getcwd(),
        filetypes=[("Text files", "*.txt")]
    )

    handle = mock_asksaveasfile.return_value.__enter__.return_value
    handle.write.assert_called_once_with(expected_content + "\n")


@patch("threading.Thread")
@patch("tkinter.Label.configure")
def test_loading(mock_label_configure, mock_thread, program):
    program.loading()
    mock_label_configure.assert_called_with(text="Загрузка...")
    mock_thread.assert_called_once_with(target=program.analyze)
    mock_thread.return_value.start.assert_called_once()


@patch("tkinter.Tk.destroy")
def test_close_app(mock_destroy, program):
    program.close_app()
    mock_destroy.assert_called_once()


@patch("tkinter.messagebox.showinfo")
def test_show_info(mock_showinfo, program, capsys):
    program.show_info()

    mock_showinfo.assert_called_once_with(
        title="О программе",
        message='"Программа создана в рамках дисциплины ТРПО"\n©Чашкин, Падалица, Маршутина, Степченко'
    )

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
