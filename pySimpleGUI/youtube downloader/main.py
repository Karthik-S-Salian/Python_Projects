import PySimpleGUI as sg
from pytube import YouTube 
import threading

file_path="F:/Users\Dell\Videos"
dl_thread=None
download_status=["--NONE-- ","--ON PROGRESS--","--COMPLETE--"]

def on_download_complete(stream,file_path):
    print("complete")
    window['-status-'].update("--COMPLETE--")

def YouTube_download(url:str,download_file=None,only_audio=False,filename=None):
    yt = YouTube(url) 
    
    if only_audio:
        stream=yt.streams.filter(progressive=True,only_audio=True,file_extension='mp4')[0]
    else:
        stream=yt.streams.filter(progressive=True,file_extension='mp4').get_highest_resolution()
        
    if stream:
        try:
            print("here")
            yt.register_on_complete_callback(on_download_complete)
            window['-status-'].update("--ON PROGRESS--")
            stream.download(output_path=download_file,filename=filename)
            
        except:
            raise Exception("couldn't download error during download check your internet connection")
    else:
        raise Exception("Couldn't find any stream")



sg.theme('GrayGrayGray')

layout=[
    [sg.Text("URL"),sg.Push(),sg.InputText(key="-url-")],
    [sg.Text("Filename"),sg.InputText(key="-filename-")],
    [sg.Text("F:/Users\Dell\Videos",key="-downloc-"),sg.Push(),sg.Button("Browse")],
    [sg.Checkbox(" audio only ",key = '-ISAUDIO-'),sg.Push(),sg.Button("download")],
    [sg.Push(),sg.Text("--NONE--",key="-status-"),sg.Push()]
    ]

window=sg.Window("YouTube Downloader",layout)

while True:
    event,values=window.read()

    if event ==sg.WIN_CLOSED:
        break

    if event == 'Browse':
        file_path = sg.popup_get_file('open',no_window = True)
        if file_path:
            window['-downloc-'].update(file_path)
    if event=="download":
        print("download!")
        dl_thread=threading.Thread(target=YouTube_download, args=(values["-url-"],file_path,values['-ISAUDIO-'],values["-filename-"]))
        dl_thread.start()
window.close()
