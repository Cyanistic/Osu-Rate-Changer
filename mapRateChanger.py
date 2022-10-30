import os
from pydub import AudioSegment

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

# Check osuRateConfig.cfg file for existing osu! directory
if os.path.exists("osuRateConfig.cfg") and os.path.exists(open("osuRateConfig.cfg", "r").readline()):
    path = open("osuRateConfig.cfg", "r").readline()

# Asks for osu! directory when no valid osuRateConfig.cfg path is found
else:
    print("No valid config detected, creating new config file\n")
    path = input("Enter your osu! Songs directory: ")
    while not os.path.exists(path):
        print("Directory not found, please try again")
        path = input("Enter your osu! Songs directory: ")
    if not (path.endswith("/") or path.endswith('\\')):
        if "/" in path: path += "/"
        else: path += "\\"
    config = open("osuRateConfig.cfg", "w").write(path)

# Creates an array to store all difficulties in song folder
songs = []

os.chdir(path)
folder = input("Enter name of the folder in which the song is in: ")

while not os.path.exists(path + folder):
    print("Folder not found!")
    folder = input("Enter name of the folder in which the song is in: ")

path += folder
os.chdir(path)

for file in os.listdir():
    if file.endswith(".osu"):
        songs.append(file)

if len(songs) > 1:
    for i in range(len(songs)):
        print(f"{i} - {songs[i]}")
    choice = int(input("Enter the number of the file: "))
    choice = songs[choice]

else:
    choice = songs[0]

# Asks user for scale factor and new rate
print("Choose a scale factor:\n 1. Scale by BPM (NOT WORKING)\n 2. Scale by Rate")
if input() == "1":
    rate = float(input("Enter the new BPM: "))
else:
    rate = float(input("Enter the new Rate: "))
mapData = open(choice, "r").readlines()

# Updates .osu file map data to correspond with new audio and file
for line in range(len(mapData)):
    if mapData[line].startswith("AudioFilename:"):
        extension = mapData[line][mapData[line].rindex(".")+1:].strip()
        audio = mapData[line][14 : mapData[line].find(extension)-1].strip()
        mapData[line] = f"{mapData[line][:14]}{audio} ({rate}x).{extension}\n"
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
    userAR = int(
        input("Enter the new approach rate for map (enter 0 to leave unchanged): ")
    )
    while 0 > userAR or userAR > 10:
        print("Invalid Approach Rate!\n")
        userAR = int(
            input("Enter the new approach rate for map (enter 0 to leave unchanged): ")
        )
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
finAudio = AudioSegment.from_file(f"{path}/{audio}.{extension}", format=extension)
fileExport = speedChange(finAudio, rate).export(f"{path}/{audio} ({rate}x).{extension}", format=extension)

# Exports .osu! data to a file
fileSave = open(f"{choice[:choice.find('.osu')]} ({rate}x).osu", "w+")
for line in mapData:
    fileSave.write(line)
print("New difficulty and audio successfully created!")