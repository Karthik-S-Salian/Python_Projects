from random import choices

import PySimpleGUI as sg
from pandas.io import clipboard
from ctypes import windll

word_list = None


def copy_dummy_text(length, size):
    try:
        length = int(length)
        size = int(size)
    except ValueError:
        return
    text = ""
    count = 0
    for word in choices(word_list, k=length):
        count += len(word)
        if count // size:
            count = len(word)
            text += "\n"
        text += word + " "

    if text:
        clipboard.copy(text)


sg.theme("DarkBlue3")
sg.set_options(font=("Courier New", 14))

layout = [
    [sg.Input(key='SIZE_INPUT', size=(10, None)),
     sg.Input("140", key='LINE_SIZE', size=(10, None)),
     sg.Button('COPY', key='-COPY-'),
     sg.Button('CLEAR', key='-CLEAR-')
     ]

]

if __name__ == "__main__":
    with open("words_new.txt", "r") as f:
        word_list = f.read().split(",")

    window = sg.Window('Title', layout, finalize=True)
    window['SIZE_INPUT'].bind("<Return>", "_Enter")

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "SIZE_INPUT" + "_Enter" or event == "-COPY-":
            copy_dummy_text(values["SIZE_INPUT"], values["LINE_SIZE"])
        elif event == "-CLEAR-":
            if windll.user32.OpenClipboard(None):
                windll.user32.EmptyClipboard()
                windll.user32.CloseClipboard()

    window.close()
