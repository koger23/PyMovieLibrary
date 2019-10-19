import os, json, sys, time

configFile = "config.json"
ICONS = os.path.dirname(__file__).replace("utils", "images")

def getIcon(iconName):

    icons = {"folder":os.path.join(ICONS, "icon_folder.png"),
             "collectingData":os.path.join(ICONS, "defaultIcon.png"),
             "style":os.path.join(ICONS, "style.qss"),
             "watchedicon":os.path.join(ICONS, "icon_checked.png"),
             "watchedfiltericon":os.path.join(ICONS, "icon_watchList.png")}
    return icons[iconName]


def getMovies(folderPath):
    return [os.path.join(folderPath, i) for i in os.listdir(folderPath) if i.endswith(".mkv")]


def saveConfig(data):

    with open(configFile, "w") as dataFile:
        json.dump(data, dataFile)

def loadConfig():

    if not os.path.exists(configFile):
        return {"folders":[]}

    with open(configFile, "r") as dataFile:
        datas = json.load(dataFile)
        return datas

def saveMovieData(path, data):
    with open(path, "w") as dataFile:
        json.dump(data, dataFile)

def loadMovieData(path):
    with open(path, "r") as dataFile:
        return json.load(dataFile)

def deleteMovieFile(path):
    if os.path.exists(path):
        os.remove(path)
