from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import os
import csv
import time
from dotenv import load_dotenv
from datetime import datetime

from src.tkb_layout import *
from src.globals import *


load_dotenv()


def init_driver():
    opts = Options()
    opts.add_argument("--incognito")
    ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    opts.add_argument("user-agent={}".format(ua))
    return webdriver.Chrome(options=opts)


def wait_value(driver, by_value, element_value, timeout=10):
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_value, element_value)))


def wait_alert(driver):
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    

def handle_alert(driver, accept=True):
    if accept:
        driver.switch_to.alert.accept()
    else:
        driver.switch_to.alert.dismiss()


def login(driver, username, password, op_timeout=0.3):
    driver.get(HOME_PAGE)

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, LOGIN_BUTTON)))
    time.sleep(op_timeout)

    login_button = driver.find_element(By.XPATH, LOGIN_BUTTON)
    login_button.click()

    time.sleep(op_timeout)
    window_login = driver.window_handles[1]
    driver.switch_to.window(window_login)

    wait_value(driver, By.XPATH, FIELD_USERNAME)
    time.sleep(op_timeout)
    field_username = driver.find_element(By.XPATH, FIELD_USERNAME)
    field_username.send_keys(username)

    wait_value(driver, By.XPATH, FIELD_PASSWORD)
    time.sleep(op_timeout)
    field_password = driver.find_element(By.XPATH, FIELD_PASSWORD)
    field_password.send_keys(password)

    wait_value(driver, By.XPATH, LOGIN_SENT_BUTTON)
    time.sleep(op_timeout)
    login_sent_button = driver.find_element(By.XPATH, LOGIN_SENT_BUTTON)
    login_sent_button.click()

    wait_alert(driver)
    handle_alert(driver)


def get_booking_info():
    info = dict()
    with open('config/book_config.csv', 'r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row[0] == 'session':
                info[row[0]] = [int(s) for s in row[1:]]
            else:
                info[row[0]] = int(row[1])

    return info['subject'], info['classroom'], info['session']


def book(driver, op_timeout=0.3):
    print('==== 預約 TKB 數位學堂 (前一日) ====')
    subject, classroom, sessions = get_booking_info()

    time.sleep(op_timeout)
    subject_select = Select(driver.find_element(By.XPATH, SUBJECT_SELECT))
    subject_select.select_by_index(subject)

    # Select the latest date
    time.sleep(op_timeout)
    date_select = Select(driver.find_element(By.XPATH, DATE_SELECT))
    date_select.select_by_index(len(date_select.options)-1)

    time.sleep(op_timeout)
    classroom_select = Select(driver.find_element(By.XPATH, CLASSROOM_SELECT))
    classroom_select.select_by_index(classroom)

    time.sleep(op_timeout)
    reserve_success, reserve_session = False, ''
    for session in sessions:
        session_box = driver.find_elements(By.NAME, SESSION_TIME_NAME)[session-1]
        if session_box.get_attribute('disabled') is None:
            session_box.click()
            reserve_success = True

            wait_value(driver, By.ID, SESSION_TIME_DIV_ID)
            sessions = driver.find_element(By.ID, SESSION_TIME_DIV_ID).get_attribute('innerText')
            reserve_session = sessions.split('\n')[session-1]
            break


    driver.find_element(By.XPATH, BOOK_BUTTON).click()
    
    wait_alert(driver)
    handle_alert(driver)

    # Successfully booked
    wait_alert(driver)
    handle_alert(driver)

    time.sleep(30)
    return reserve_success, reserve_session


def reserve_latest():
    driver = init_driver()
    login(driver, os.getenv('USERNAME'), os.getenv('PASSWORD'))
    success, session = book(driver)
    driver.close()
    return success, session


def after(target_time):
    current_time = datetime.now()
    return current_time >= target_time


def main():
    midnight = datetime.now()
    if midnight.hour != 0:
        midnight = midnight.replace(
            day=midnight.day+1,
            hour=0, minute=0, second=0,
            microsecond=0
        )

    while True:
        print(f'current time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'target time:  {midnight.strftime("%Y-%m-%d %H:%M:%S")}')
        if after(midnight):
            success, session = reserve_latest()
            if success:
                print(f'TKB 預約位置完成: {session}')
            else:
                print(f'TKB 位置預約失敗，所有位置均已搶完')
            break
        time.sleep(1)
        os.system('clear')


if __name__ == '__main__':
    main()