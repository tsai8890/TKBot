import os
import PySimpleGUI as sg

from datetime import datetime
from datetime import date, timedelta

import modules.globals as globals


def after(target_time):
    current_time = datetime.now()
    return current_time >= target_time


def create_window():
    subject_l = [
        sg.Text('輸入上課資訊', size=(15, 1), font=30),
        sg.Combo(
            globals.tkb_data['subjects'], key='subject', 
            size=(15, 10), font=15
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
            [classroom[0] for classroom in globals.tkb_data['classrooms']], key='classroom',
            size=(20, 10), font=20, enable_events=True
        )
    ]

    session_left_column = [
        [sg.Text('欲上課時間', size=(14, 1), font=20)]
    ]
    
    session_right_column = [
        [sg.Checkbox('', key=f'session_{i}', font=30, visible=False)]
        for i in range(globals.MAX_SESSIONS)
    ]
    
    session_l = [
        sg.Column(session_left_column),
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


def main_loop(tkb_agent):
    midnight = datetime.now() + timedelta(days=1)
    midnight = midnight.replace(
        hour=0, minute=0, second=0,
        microsecond=0
    )

    tkb_agent.login()
    reserved = False
    window = create_window()
    while True:
        event, values = window.read(timeout=20)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == 'classroom':
            day_key = 'weekday'
            if midnight.weekday() == 5:
                day_key = 'saturday'
            elif midnight.weekday() == 6:
                day_key = 'sunday'
            
            classroom_id = -1
            for i, (classroom, _) in enumerate(globals.tkb_data['classrooms']):
                if classroom == values['classroom']:
                    classroom_id = i

            for i in range(globals.MAX_SESSIONS):
                if i < len(globals.tkb_data['classrooms'][classroom_id][1][day_key]):
                    window[f'session_{i}'].update(
                        text=globals.tkb_data['classrooms'][classroom_id][1][day_key][i][1],
                        disabled=(globals.tkb_data['classrooms'][classroom_id][1][day_key][i][0] is False),
                        visible=True, value=False
                    )
                else:
                    window[f'session_{i}'].update(visible=False, value=False)

            tkb_agent.set_booking_info(classroom=classroom_id)

        elif event == 'Reserve':
            subject_id = -1
            for i, subject in enumerate(globals.tkb_data['subjects']):
                if subject == values['subject']:
                    subject_id = i

            tkb_agent.set_booking_info(
                subject=subject_id,
                sessions=[i for i in range(globals.MAX_SESSIONS) if values[f'session_{i}']]
            )

            window['waiting'].update(visible=True)
            reserved = True

            os.system('clear')
            print('==== 預約 TKB 數位學堂 ====')
            print(f'科目: {tkb_agent.subject}')
            print(f'上課地點: {tkb_agent.classroom}')
            print(f'上課時間: {tkb_agent.sessions}')

        # Reservation
        if reserved:
            if after(midnight):
                reserved_sessions = tkb_agent.book()
                if len(reserved_sessions) != 0:
                    print(f'預約成功: {reserved_sessions}')
                else:
                    print('預約失敗: 已經全數額滿')
            break

    window.close()