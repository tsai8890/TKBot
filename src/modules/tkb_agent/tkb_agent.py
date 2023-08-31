from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import os
import time
import json
from dotenv import load_dotenv

import modules.tkb_agent.tkb_layout as tkb_layout


class TKB_Agent:
    def __init__(self):
        load_dotenv()
        self.USERNAME = os.getenv('USERNAME')
        self.PASSWORD = os.getenv('PASSWORD')
        self.init_driver()


    def init_driver(self):
        opts = Options()
        # opts.add_argument("--incognito")
        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        opts.add_argument("user-agent={}".format(ua))
        self.driver = webdriver.Chrome(options=opts)
    

    def set_booking_info(self, subject=None, classroom=None, sessions=None):
        if subject is not None:
            self.subject = subject
        if classroom is not None:
            self.classroom = classroom
        if sessions is not None:
            self.sessions = sessions


    def login_manually(self):
        self.driver.get(tkb_layout.HOME_PAGE)
        while True:
            try:
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.find_element(By.XPATH, tkb_layout.LOGIN_STATUS_BUTTON)
                self.driver.find_element(By.XPATH, tkb_layout.LOGIN_STATUS_TEXT)
                break
            except:
                pass
        print('successfully loginned')


    def login(self, op_timeout=0.3):
        self.driver.get(tkb_layout.HOME_PAGE)

        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, tkb_layout.LOGIN_BUTTON)))
        time.sleep(op_timeout)

        login_button = self.driver.find_element(By.XPATH, tkb_layout.LOGIN_BUTTON)
        login_button.click()

        time.sleep(op_timeout)
        window_login = self.driver.window_handles[1]
        self.driver.switch_to.window(window_login)

        self.wait_value(self.driver, By.XPATH, tkb_layout.FIELD_USERNAME)
        time.sleep(op_timeout)
        field_username = self.driver.find_element(By.XPATH, tkb_layout.FIELD_USERNAME)
        field_username.send_keys(self.USERNAME)

        self.wait_value(self.driver, By.XPATH, tkb_layout.FIELD_PASSWORD)
        time.sleep(op_timeout)
        field_password = self.driver.find_element(By.XPATH, tkb_layout.FIELD_PASSWORD)
        field_password.send_keys(self.PASSWORD)

        self.wait_value(self.driver, By.XPATH, tkb_layout.LOGIN_SENT_BUTTON)
        time.sleep(op_timeout)
        login_sent_button = self.driver.find_element(By.XPATH, tkb_layout.LOGIN_SENT_BUTTON)
        login_sent_button.click()

        self.wait_alert(self.driver)
        self.handle_alert(self.driver)


    def book(self, op_timeout=0):
        # Select the subject
        time.sleep(op_timeout)
        self.wait_value(self.driver, By.XPATH, tkb_layout.SUBJECT_SELECT)
        subject_select = Select(self.driver.find_element(By.XPATH, tkb_layout.SUBJECT_SELECT))
        subject_select.select_by_index(self.subject + 1)

        # Select the latest date
        time.sleep(op_timeout)
        self.wait_value(self.driver, By.XPATH, tkb_layout.DATE_SELECT)
        date_select = Select(self.driver.find_element(By.XPATH, tkb_layout.DATE_SELECT))
        date_select.select_by_index(len(date_select.options)-1)

        # Select the classroom
        time.sleep(op_timeout)
        self.wait_value(self.driver, By.XPATH, tkb_layout.CLASSROOM_SELECT)
        classroom_select = Select(self.driver.find_element(By.XPATH, tkb_layout.CLASSROOM_SELECT))
        classroom_select.select_by_index(self.classroom + 1)

        # Select the session
        time.sleep(op_timeout)
        self.wait_value(self.driver, By.ID, tkb_layout.SESSION_TIME_DIV_ID)

        sessions_text = self.driver.find_element(By.ID, tkb_layout.SESSION_TIME_DIV_ID).get_attribute('innerText')
        reserved_sessions = []
        for session in self.sessions:
            self.wait_value(self.driver, By.NAME, tkb_layout.SESSION_TIME_NAME)
            session_box = self.driver.find_elements(By.NAME, tkb_layout.SESSION_TIME_NAME)[session]
            if session_box.get_attribute('disabled') is None:
                session_box.click()
                reserved_sessions.append(sessions_text.split('\n')[session])
        
        # Submit the form
        self.driver.find_element(By.XPATH, tkb_layout.BOOK_BUTTON).click()
        self.wait_alert(self.driver)
        self.handle_alert(self.driver)

        # Successfully booked
        self.wait_alert(self.driver)
        self.handle_alert(self.driver)
        self.driver.save_screenshot('booking_success.png')
        return reserved_sessions

    
    def update_tkb_data(self):
        self.login_manually()
        tkb_data = {
            'subjects': [], 'classrooms': []
        }

        # Record all the subjects and choose the first subject for the following operations
        self.wait_value(self.driver, By.XPATH, tkb_layout.SUBJECT_SELECT)
        subject_select = Select(self.driver.find_element(By.XPATH, tkb_layout.SUBJECT_SELECT))
        for subject in subject_select.options[1:]:
            tkb_data['subjects'].append(subject.text)
        subject_select.select_by_index(1)

        # Only choosing one date first can we view the classroom informations
        self.wait_value(self.driver, By.XPATH, tkb_layout.DATE_SELECT)
        date_select = Select(self.driver.find_element(By.XPATH, tkb_layout.DATE_SELECT))
        date_select.select_by_index(1)

        # Choose each classroom, record them, and record their respective available sessions
        self.wait_value(self.driver, By.XPATH, tkb_layout.CLASSROOM_SELECT)
        classroom_select = Select(self.driver.find_element(By.XPATH, tkb_layout.CLASSROOM_SELECT))
        for i, classroom in enumerate(classroom_select.options):
            if i == 0:
                continue

            tkb_data['classrooms'].append([classroom.text, dict()])
            
            classroom_select.select_by_index(i)
            self.wait_value(self.driver, By.XPATH, tkb_layout.DATE_SELECT)
            date_select = Select(self.driver.find_element(By.XPATH, tkb_layout.DATE_SELECT))
            for j, date_item in enumerate(date_select.options):
                if j == 0:
                    continue
                
                date_select.select_by_index(j)
                print(i, j)
                print(classroom.text, date_item.text)
                self.wait_value(self.driver, By.ID, tkb_layout.SESSION_TIME_DIV_ID)
                sessions_text = self.driver.find_element(By.ID, tkb_layout.SESSION_TIME_DIV_ID).get_attribute('innerText')
                sessions_text = sessions_text.split('\n')[:-1]
                
                session_type = ''
                if date_item.text[-1] == '一':
                    session_type = 'weekday'
                elif date_item.text[-1] == '六':
                    session_type = 'saturday'
                elif date_item.text[-1] == '日':
                    session_type = 'sunday'
                else:
                    continue

                tkb_data['classrooms'][-1][1][session_type] = []
                for session in sessions_text:
                    if session[-4:] == '己停課)':
                        # The TKB's website used the character '己' instead of '已'
                        tkb_data['classrooms'][-1][1][session_type].append([False, session])
                    elif session[-4:] == '已滿場)' or session[-4:] == '已預約)':
                        tkb_data['classrooms'][-1][1][session_type].append([True, session[:-8]])
                    else:
                        tkb_data['classrooms'][-1][1][session_type].append([True, session])

        with open('src/gui/tkb_data_new.json', 'w', encoding='utf-8') as f:
            json.dump(tkb_data, f, ensure_ascii=False, indent=4)


    def wait_value(self, driver, by_value, element_value, timeout=10):
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_value, element_value)))


    def wait_alert(self, driver):
        WebDriverWait(driver, 10000).until(EC.alert_is_present())
        

    def handle_alert(self, driver, accept=True):
        if accept:
            driver.switch_to.alert.accept()
        else:
            driver.switch_to.alert.dismiss()