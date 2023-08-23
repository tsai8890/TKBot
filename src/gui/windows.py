import PySimpleGUI as sg
import json
from datetime import date, timedelta


def empty_block(size=(15,1)):
    return sg.Text('', size=size)


def create_window():
    tkb_data = None
    with open('src/gui/tkb_data.json') as file:
        tkb_data = json.load(file)

    subject_l = [
        sg.Text('輸入上課資訊', size=(15, 1), font=30),
        sg.Combo(
            tkb_data['subjects'], key='subject', 
            default_value=tkb_data['subjects'][0], size=(15, 10), font=15
        )
    ]

    date_l = [
        sg.Text('欲上課日期', size=(15, 1), font=20),
        sg.Combo(
            [f'{date.today() + timedelta(days=7)}'], 
            key='date', default_value=f'{date.today() + timedelta(days=7)}', size=(15, 10), font=20
        )
    ]

    classroom_l = [
        sg.Text('上課教室', size=(15, 1), font=20),
        sg.Combo(
            tkb_data['classrooms'], key='classroom',
            default_value=tkb_data['classrooms'][0], size=(20, 10), font=20
        )
    ]

    session_left_column = [
        [sg.Text('欲上課時間', size=(14, 1), font=20)]
    ]

    session_right_column = [
        [sg.Checkbox(session, key=session, font=30)]
        for session in tkb_data['sessions']['(24)林口數位學堂']
    ]

    session_l = [
        sg.Column(session_left_column),
        sg.VSeparator(),
        sg.Column(session_right_column)
    ]

    reserve_l = [
        sg.Button('預約', key='Reserve', font=('Times New Roman',20)), 
        sg.Button('結束', key='Exit', font=('Times New Roman',20))
    ]

    waiting_l = [
        sg.Text('已預約，等待中 ...', key='waiting', font=30, visible=False)
    ]

    layout = [
        subject_l,
        date_l,
        classroom_l,
        session_l,
        reserve_l,
        waiting_l
    ]
    return sg.Window('TKB 數位學堂 預約位置系統', layout, size=(500, 500))
