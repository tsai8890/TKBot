import sys
sys.dont_write_bytecode = True

import os
import json
import PySimpleGUI as sg
from datetime import datetime

from src.gui.windows import create_window
from src.tkb_agent.tkb_agent import TKB_Agent


def after(target_time):
    current_time = datetime.now()
    return current_time >= target_time


def main():
    tkb_data = None
    with open('src/gui/tkb_data.json') as file:
        tkb_data = json.load(file)
        
    tkb_agent = TKB_Agent()
    tkb_agent.set_tkb_info(
        tkb_data['subjects'][0],
        tkb_data['classrooms'][0],
        tkb_data['sessions']['(24)林口數位學堂'][0]
    )
    tkb_agent.login()

    midnight = datetime.now()
    if midnight.hour != 0:
        midnight = midnight.replace(
            day=midnight.day+1,
            hour=0, minute=0, second=0,
            microsecond=0
        )

    reserved = False
    window = create_window()
    while True:
        event, values = window.read(timeout=20)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
        if event == 'Reserve':
            tkb_agent.set_tkb_info(
                values['subject'],
                values['classroom'],
                [session for session in tkb_data['sessions']['(6)新莊中正數位學堂'] if values[session]]
            )
            window['waiting'].update(visible=True)
            reserved = True

            os.system('clear')
            print('==== 預約 TKB 數位學堂 ====')
            print(f'科目: {tkb_agent.subject}')
            print(f'上課地點: {tkb_agent.classroom}')
            print(f'上課時間: {tkb_agent.sessions}')

        if reserved:
            if after(midnight):
                reserved_sessions = tkb_agent.book()
                if len(reserved_sessions) != 0:
                    print(f'預約成功: {reserved_sessions}')
                else:
                    print(f'預約失敗: 已經全數額滿')
                break

    window.close()
    # tkb_agent.driver.quit()


if __name__ == '__main__':
    main()