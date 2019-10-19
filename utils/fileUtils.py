import json
import os

configFile = "config.json"
ICONS = os.path.dirname(__file__).replace("utils", "images")


def get_icon(icon_name):
    icons = {"folder": os.path.join(ICONS, "icon_folder.png"),
             "collectingData": os.path.join(ICONS, "defaultIcon.png"),
             "style": os.path.join(ICONS, "style.qss"),
             "watchedicon": os.path.join(ICONS, "icon_checked.png"),
             "watchedfiltericon": os.path.join(ICONS, "icon_watchList.png")}
    return icons[icon_name]


def get_movies(folder_path):
    return [os.path.join(folder_path, i) for i in os.listdir(folder_path) if i.endswith(".mkv")]


def save_config(data):
    with open(configFile, "w") as dataFile:
        json.dump(data, dataFile)


def load_config():
    if not os.path.exists(configFile):
        return {"folders": []}

    with open(configFile, "r") as dataFile:
        datas = json.load(dataFile)
        return datas


def save_movie_data(path, data):
    with open(path, "w") as dataFile:
        json.dump(data, dataFile)


def load_movie_data(path):
    with open(path, "r") as dataFile:
        return json.load(dataFile)


def delete_movie_file(path):
    if os.path.exists(path):
        os.remove(path)
