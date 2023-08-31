import json


def init_globals():
    # tkb_data
    global tkb_data
    file = open('modules/resources/tkb_data.json')
    tkb_data = json.load(file)

    global MAX_SESSIONS
    MAX_SESSIONS = 6
