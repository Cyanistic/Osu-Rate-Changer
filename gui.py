import PySimpleGUI as sg
import os

def generateFile(audioPath,Rate):
    pass

sg.theme('dark grey 9')

if os.path.exists("osuRateConfig.cfg") and os.path.exists(open("osuRateConfig.cfg", "r").readline()):
    path = open("osuRateConfig.cfg", "r").readline()
else:
    dirLayout = [[sg.Text("Enter the path of your osu! songs folder: ")],[sg.Input(key = "dirInput")],[sg.Button("Submit", key = "dirButton")]]
    osuDir = sg.Window("Converter", dirLayout)
    while True:
        event, values = osuDir.read()
        if event == "dirButton" and os.path.exists(values["dirInput"]):
            path = values["dirInput"]
            if not (path.endswith("/") or path.endswith('\\')):
                if "/" in path: path += "/"
                else: path += "\\"
            config = open("osuRateConfig.cfg", "w").write(path)
            break
            
        if event == sg.WIN_CLOSED:
            break
    osuDir.close()

os.chdir(path)
folderList = sg.Combo(sorted(os.listdir()), size = (40,8), key = "folders")
diffList = sg.Listbox(list([]), size=(50,6), enable_events=False, key='_LIST_')
layout = [
    [sg.Text("Folder Name: "), folderList, sg.Button("Search/Select", key = "searchButton")],
    [sg.Text("Difficulty: "), diffList], 
    [sg.Text("Rate: "),sg.Input(key = "inputRate")],
    [sg.Button("Create File and Audio", key = "submitButton"), sg.Text("", key="resultText")]
    ]

window = sg.Window("Osu Rate Changer", layout, size = (600, 200), icon ="abl")
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == "searchButton":
        updatedFolders = sorted(filter(lambda x: values["folders"] in x, os.listdir()))
        window['folders'].update(value=updatedFolders[0], values=updatedFolders)
        if(os.path.exists(path + updatedFolders[0])):
            os.chdir(path + updatedFolders[0])
            window['_LIST_'].update(filter(lambda x: x.endswith(".osu"),os.listdir()))
    elif event == "submitButton":
        try:
            print(f"{path}{updatedFolders[0]}/{values['_LIST_']}")
            generateFiles(f"{path}{updatedFolders[0]}/{diffList[0]}",float(values["inputRate"]))
        except :
            window["resultText"].update("Error, something went wrong")

window.close()