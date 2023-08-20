import PySimpleGUI as sg
import json
from datetime import date, timedelta


def create_window():
    tkb_data = None
    with open('src/gui/tkb_data.json') as file:
        tkb_data = json.load(file)

    layout = [
        [sg.Text('輸入上課資訊', font=30)],
        [
            sg.Text('科目', size=(15, 1), font=20),
            sg.Combo(
                tkb_data['subjects'], key='subject', 
                default_value=tkb_data['subjects'][0], size=(20, 10), font=15
            )
        ],
        [
            sg.Text('欲上課日期', size=(15, 1), font=20),
            sg.Combo(
                [f'{date.today() + timedelta(days=7)}'], 
                key='date', default_value=f'{date.today() + timedelta(days=7)}', size=(20, 10), font=20
            )
        ],
        [
            sg.Text('上課教室', size=(15, 1), font=20),
            sg.Combo(
                tkb_data['classrooms'], key='classroom', 
                default_value=tkb_data['classrooms'][0], size=(20, 10), font=20
            )
        ],
        [
            sg.Text('欲上課時間', size=(15, 1), font=20), 
            sg.Combo(
                tkb_data['sessions']['(24)林口數位學堂'], key='sessions', 
                default_value=tkb_data['sessions']['(24)林口數位學堂'][0], size=(20, 10), font=20
            )
        ],
        [
            sg.Button('預約', key='Reserve', font=('Times New Roman',20)), 
            sg.Button('結束', key='Exit', font=('Times New Roman',20))
        ],
        [
            sg.Text('已預約，等待中 ...', key='waiting', font=30, visible=False)
        ]
    ]
    return sg.Window('TKB 數位學堂 預約位置系統', layout, size=(500, 500))