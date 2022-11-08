import PySimpleGUI as sg
from pathlib import Path


smileys = [
	'happy',[':)','xD',':D','<3'],
	'sad',[':(','T_T'],
	'other',[':3']
]

menu_layout=[
    ["File",['Open',"Save",'---','Exit']],
    ['Tool',['word count']],
    ['Add',smileys]
]

smiley_events = smileys[1] + smileys[3] + smileys[5]


sg.theme('GrayGrayGray')

layout=[
    [sg.Menu(menu_layout)],
    [sg.Text("untitled",key="-filename-")],
    [sg.Multiline(no_scrollbar = True, size = (80,30), key = '-TEXTBOX-')],
    [sg.Button("save")]
    ]
window=sg.Window("text editor",layout)
file_path=None
while True:
    event,values=window.read()

    if event in (sg.WIN_CLOSED,'Exit'):
        break

    if event == 'Open':
        file_path = sg.popup_get_file('open',no_window = True)
        if file_path:
            file = Path(file_path)
            window['-TEXTBOX-'].update(file.read_text())
            window["-filename-"].update(file_path.split("/")[-1])
    elif event=="Save":
        if file_path:
            file.write_text(values['-TEXTBOX-'])
        else:
            file_path = sg.popup_get_file('open',no_window = True, save_as = True)+".txt"
            file=Path(file_path)
            file.write_text(values['-TEXTBOX-'])
            window["-filename-"].update(file_path.split("/")[-1])
    if event == 'word count':
        word_list = values['-TEXTBOX-'].replace('\n',' ').split(" ")
        char_count=len("".join(word_list))
        word_count=0
        if char_count:
            word_count=len(word_list)
        sg.popup(f'words {word_count}\ncharacters: {char_count}')

    if event in smiley_events:
        current_text = values['-TEXTBOX-']
        new_text = current_text + ' ' + event
        window['-TEXTBOX-'].update(new_text)

window.close()


