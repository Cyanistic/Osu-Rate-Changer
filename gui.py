import PySimpleGUI as sg
from pydub import AudioSegment
import os

# Function to make generate a new audio file with a speed change from old file
def speedChange(audio, rate):
    return audio._spawn(
        audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * rate)}
    )

# Function to find the nth occurance of a character in a string
def trimmer(string, divider, times):
    index = 0
    for i in range(times):
        index = string.find(divider, index)
        index += 1
    return index

def generateFiles(path, mapFile, rate):
    mapData = open(mapFile, "r").readlines()

    for line in range(len(mapData)):
        if mapData[line].startswith("AudioFilename:"):
            audio = mapData[line][14 : mapData[line].find(".mp3")].strip()
            mapData[line] = f"{mapData[line][:14]}{audio} ({rate}x).mp3\n"
        elif mapData[line].startswith("PreviewTime:"):
            prevTime = int(mapData[line][12:].strip())
            mapData[line] = f"{mapData[line][:12]} {int(prevTime/rate)}\n"
        elif mapData[line].startswith("Mode:"):
            gamemode = int(mapData[line][5:].strip())
        elif mapData[line].startswith("Version:"):
            diffName = mapData[line][8:].strip()
            mapData[line] = f"{mapData[line][:8]}{diffName} ({rate}x)\n"
            break

    # Uses the formula for the corresponding gamemode and modifies the rate of the map in the .osu file
    startIndex = mapData.index("[HitObjects]\n") + 1
    for line in range(mapData.index("[TimingPoints]\n")+1,startIndex):
        try:
            mapData[line] = f"{int(int(mapData[line][:mapData[line].index(',')])/rate)}{mapData[line][mapData[line].index(','):]}"
        except:
            pass
    if gamemode == 0:
        arPopup = sg.Window("AR Popup", [[sg.Text("Enter new AR (Enter 0 to leave unchanged)")],[sg.Input(key="arBox")],[sg.Button("Submit")],[sg.Text("", key = "result")]])
        while True:
            event, values = arPopup.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == "Submit":
                try:
                    userAR = float(values["arBox"])
                    if 0 > userAR or userAR > 10: raise Exception()
                    break
                except:
                    window["result"].update("Invalid AR!")
        arPopup.close()
        if not userAR == 0:
            for line in range(len(mapData)):
                if mapData[line].startswith("ApproachRate:"):
                    mapData[line] = f"ApproachRate:{userAR}\n"
        for line in range(startIndex, len(mapData)):
            try:
                commaIndex = trimmer(mapData[line], ",", 2)
                storage = f'{mapData[line][:commaIndex]}{int(int(mapData[line][commaIndex:mapData[line].find(",", commaIndex+1)])/rate)}'
                if ("|" in mapData[line]) or (trimmer(mapData[line], ",", 6) < 5):
                    storage += f'{mapData[line][trimmer(mapData[line], ",", 3)-1:]}'
                else:
                    storage += f'{mapData[line][trimmer(mapData[line], ",", 3)-1:trimmer(mapData[line], ",", 5)]}{int(int(mapData[line][trimmer(mapData[line], ",", 5):trimmer(mapData[line], ",", 6)-1])/rate)}{mapData[line][trimmer(mapData[line], ",", 6)-1:]}'

                mapData[line] = storage
            except:
                pass
    elif gamemode == 1:
        for line in range(startIndex, len(mapData)):
            try:
                commaIndex = trimmer(mapData[line], ",", 2)
                mapData[line] = f'{mapData[line][:commaIndex]}{int(int(mapData[line][commaIndex:mapData[line].find(",", commaIndex+1)])/rate)}{mapData[line][trimmer(mapData[line], ",", 3)-1:]}'
            except:
                pass
    elif gamemode == 2:
        for line in range(startIndex, len(mapData)):
            try:
                commaIndex = trimmer(mapData[line], ",", 2)
                storage = f'{mapData[line][:commaIndex]}{int(int(mapData[line][commaIndex:mapData[line].find(",", commaIndex+1)])/rate)}'
                if ("|" in mapData[line]) or (trimmer(mapData[line], ",", 6) < 5):
                    storage += mapData[line][trimmer(mapData[line], ",", 3) - 1 :]
                else:
                    storage += f'{mapData[line][trimmer(mapData[line], ",", 3)-1:trimmer(mapData[line], ",", 5)]}{int(int(mapData[line][trimmer(mapData[line], ",", 5):trimmer(mapData[line], ",", 6)-1])/rate)}{mapData[line][trimmer(mapData[line], ",", 6)-1:]}'

                mapData[line] = storage
            except:
                pass
    elif gamemode == 3:
        for line in range(startIndex, len(mapData)):
            try:
                commaIndex = trimmer(mapData[line], ",", 2)
                mapData[line] = f'{mapData[line][:commaIndex]}{int(int(mapData[line][commaIndex:mapData[line].find(",", commaIndex+1)])/rate)}{mapData[line][trimmer(mapData[line], ",", 3)-1:trimmer(mapData[line], ",", 5)]}{int(int(mapData[line][trimmer(mapData[line], ",", 5):mapData[line].find(":")])/rate)}{mapData[line][mapData[line].find(":"):]}'
            except:
                pass
    else:
        print("uh waltuh")

    # Creates new audio file with rate change
    mp3Audio = AudioSegment.from_file(f"{path}/{audio}.mp3", format="mp3")
    fileExport = speedChange(mp3Audio, rate).export(f"{path}/{audio} ({rate}x).mp3", format="mp3")

    # Exports .osu! data to a file
    fileSave = open(f"{mapFile[:mapFile.find('.osu')]} ({rate}x).osu", "w+")
    for line in mapData:
        fileSave.write(line)

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
diffList = sg.Listbox(list([]), size = (100,6), enable_events=True, key='_LIST_')
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
        os.chdir(path)
        updatedFolders = sorted(filter(lambda x: values["folders"].lower() in x.lower(), os.listdir()))
        try:
            if(values["folders"].lower() == updatedFolders[updatedFolders.index(values["folders"])].lower()): updatedFolders = [updatedFolders[updatedFolders.index(values["folders"])]]
        except:
            updatedFolders = sorted(filter(lambda x: values["folders"].lower() in x.lower(), os.listdir()))
        window['folders'].update(value=updatedFolders[0], values=updatedFolders)
        if(os.path.exists(path + updatedFolders[0])):
            os.chdir(path + updatedFolders[0])
            songs = list(filter(lambda x: x.endswith(".osu"),os.listdir()))
            window['_LIST_'].update(songs)
    elif event == "submitButton":
        
        try:
            chosenDiff = songs[window.Element('_LIST_').Widget.curselection()[0]]
            window["resultText"].update("Working...")
            generateFiles(path + updatedFolders[0],chosenDiff,float(values["inputRate"]))
            window["resultText"].update("New difficulty and audio successfully created! Search for an empty string to change the rate of another map!")
        except ValueError:
            window["resultText"].update("Error, Invalid Rate")
        except:
            window["resultText"].update("Error, Something Went Wrong")

window.close()