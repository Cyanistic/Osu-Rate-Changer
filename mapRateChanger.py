import re
import os
from pydub import AudioSegment

def speedChange(audio, rate):
    newAudio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * rate)})
    return newAudio
def trimmer(string, divider, times):
    index = 0
    for i in range(times):
        index = string.find(divider, index)
        index +=1
    return index

if(os.path.exists("config.cfg") and os.path.exists(open("config.cfg", "r").readline())):
    path = open("config.cfg", "r").readline()

else:
    print("No config valid detected, creating new config file\n")
    path = input("Enter your osu! Songs directory: ")
    while (not os.path.exists(path)):
        print("Directory not found, please try again")
        path = input("Enter your osu! Songs directory: ")
    config = open("config.cfg", "w").write(path)

songs = []
os.chdir(path)
folder = input("Enter name of the folder in which the song is in: ")

while(not os.path.exists(path + folder)):
    print("Folder not found!")
    folder = input("Enter name of the folder in which the song is in: ")

path += folder
os.chdir(path)

for file in os.listdir():
    if file.endswith(".osu"):
            songs.append(file)
    
if(len(songs) > 1):
    for i in range(len(songs)):
        print(f"{i} - {songs[i]}")
    choice = int(input("Enter the number of the file: "))
    choice = songs[choice]

else:
    choice = songs[0]
print("Choose a scale factor:\n 1. Scale by BPM (NOT WORKING)\n 2. Scale by Rate")
if(input() == "1"):
    rate = float(input("Enter the new BPM: "))
else:
    rate = float(input("Enter the new Rate: "))
mapData = open(choice, "r").readlines()

for line in range(len(mapData)):
    if(mapData[line].startswith("AudioFilename:")):
        audio = mapData[line][14:mapData[line].find(".mp3")].strip()
        mapData[line] = f"{mapData[line][:14]}{audio} ({rate}x).mp3\n"
    elif(mapData[line].startswith("PreviewTime:")):
        prevTime = int(mapData[line][12:].strip())
        mapData[line] = f"{mapData[line][:12]} {int(prevTime/rate)}\n"
    elif(mapData[line].startswith("Mode:")):
        gamemode = int(mapData[line][5:].strip())
    elif(mapData[line].startswith("Version:")):
        diffName = mapData[line][8:].strip()
        mapData[line] = f"{mapData[line][:8]}{diffName} ({rate}x)\n"
        break
startIndex = mapData.index("[HitObjects]\n")+1
if(gamemode == 0):
    userAR = int(input("Enter the new approach rate for map (enter 0 to leave unchanged): "))
    while (0 > userAR or userAR > 10):
        print("Invalid Approach Rate!\n")
        userAR = int(input("Enter the new approach rate for map (enter 0 to leave unchanged): "))
    if(not userAR == 0):
        for line in range(len(mapData)):
            if(mapData[line].startswith("ApproachRate:")): mapData[line] = f"ApproachRate:{userAR}\n"
    for line in range(startIndex, len(mapData)):
        commaIndex = trimmer(mapData[line], ",", 2)
        storage = mapData[line][:commaIndex] + str(int(int(mapData[line][commaIndex:mapData[line].find(",", commaIndex+1)])/rate))
        if(("|" in mapData[line]) or (trimmer(mapData[line], ",", 6) < 5)):
            storage += mapData[line][trimmer(mapData[line], ",", 3)-1:]
        else:
            storage += mapData[line][trimmer(mapData[line], ",", 3)-1:trimmer(mapData[line], ",", 5)] + str(int(int(mapData[line][trimmer(mapData[line], ",", 5):trimmer(mapData[line], ",", 6)-1])/rate)) + mapData[line][trimmer(mapData[line], ",", 6)-1:]
        
        mapData[line] = storage
elif (gamemode == 1):
    for line in range(startIndex, len(mapData)):
        commaIndex = trimmer(mapData[line], ",", 2)
        mapData[line] = mapData[line][:commaIndex] + str(int(int(mapData[line][commaIndex:mapData[line].find(",", commaIndex+1)])/rate)) + mapData[line][trimmer(mapData[line], ",", 3)-1:]
elif(gamemode == 2):
     for line in range(startIndex, len(mapData)):
        commaIndex = trimmer(mapData[line], ",", 2)
        storage = mapData[line][:commaIndex] + str(int(int(mapData[line][commaIndex:mapData[line].find(",", commaIndex+1)])/rate))
        if(("|" in mapData[line]) or (trimmer(mapData[line], ",", 6) < 5)):
            storage += mapData[line][trimmer(mapData[line], ",", 3)-1:]
        else:
            storage += mapData[line][trimmer(mapData[line], ",", 3)-1:trimmer(mapData[line], ",", 5)] + str(int(int(mapData[line][trimmer(mapData[line], ",", 5):trimmer(mapData[line], ",", 6)-1])/rate)) + mapData[line][trimmer(mapData[line], ",", 6)-1:]
        
        mapData[line] = storage
elif(gamemode == 3):
    for line in range(startIndex, len(mapData)):
        commaIndex = trimmer(mapData[line], ",", 2)
        mapData[line] = mapData[line][:commaIndex] + str(int(int(mapData[line][commaIndex:mapData[line].find(",", commaIndex+1)])/rate)) + mapData[line][trimmer(mapData[line], ",", 3)-1:trimmer(mapData[line], ",", 5)] + str(int(int(mapData[line][trimmer(mapData[line], ",", 5):mapData[line].find(":")])/rate)) + mapData[line][mapData[line].find(":"):]
else:
    print("uh waltuh")

mp3Audio = AudioSegment.from_file(f"{path}/{audio}.mp3", format="mp3")
newAudio = f"{audio} ({rate}x)"
fileExport = speedChange(mp3Audio, rate).export(f"{path}/{newAudio}.mp3", format="mp3")
fileSave = open(f"{choice[:choice.find('.osu')]} ({rate}x).osu","w+")
for line in mapData:
    fileSave.write(line)
print("New difficulty and audio successfully created!")
