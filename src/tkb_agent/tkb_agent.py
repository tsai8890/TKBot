from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import os
import time
from dotenv import load_dotenv

from src.tkb_layout import *
from src.globals import *


class TKB_Agent:
    def __init__(self):
        load_dotenv()
        self.USERNAME = os.getenv('USERNAME')
        self.PASSWORD = os.getenv('PASSWORD')
        self.init_driver()


    def init_driver(self):
        opts = Options()
        opts.add_argument("--incognito")
        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        opts.add_argument("user-agent={}".format(ua))
        self.driver = webdriver.Chrome(options=opts)
    

    def set_tkb_info(self, subject, classroom, sessions):
        self.subject = subject
        self.classroom = classroom
        self.sessions = sessions

    
    def login(self, op_timeout=0.3):
        self.driver.get(HOME_PAGE)

        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, LOGIN_BUTTON)))
        time.sleep(op_timeout)

        login_button = self.driver.find_element(By.XPATH, LOGIN_BUTTON)
        login_button.click()

        time.sleep(op_timeout)
        window_login = self.driver.window_handles[1]
        self.driver.switch_to.window(window_login)

        self.wait_value(self.driver, By.XPATH, FIELD_USERNAME)
        time.sleep(op_timeout)
        field_username = self.driver.find_element(By.XPATH, FIELD_USERNAME)
        field_username.send_keys(self.USERNAME)

        self.wait_value(self.driver, By.XPATH, FIELD_PASSWORD)
        time.sleep(op_timeout)
        field_password = self.driver.find_element(By.XPATH, FIELD_PASSWORD)
        field_password.send_keys(self.PASSWORD)

        self.wait_value(self.driver, By.XPATH, LOGIN_SENT_BUTTON)
        time.sleep(op_timeout)
        login_sent_button = self.driver.find_element(By.XPATH, LOGIN_SENT_BUTTON)
        login_sent_button.click()

        self.wait_alert(self.driver)
        self.handle_alert(self.driver)


    def book(self, op_timeout=0.3):
        # Select the subject
        time.sleep(op_timeout)
        subject_select = Select(self.driver.find_element(By.XPATH, SUBJECT_SELECT))
        subject_select.select_by_index(int(self.subject.split(')')[0].strip('(')))

        # Select the latest date
        time.sleep(op_timeout)
        date_select = Select(self.driver.find_element(By.XPATH, DATE_SELECT))
        date_select.select_by_index(len(date_select.options)-1)

        # Select the classroom
        time.sleep(op_timeout)
        classroom_select = Select(self.driver.find_element(By.XPATH, CLASSROOM_SELECT))
        classroom_select.select_by_index(int(self.classroom.split(')')[0].strip('(')))

        # Select the session
        time.sleep(op_timeout)
        reserve_success, reserve_session = False, ''

        sessions_id = [int(session.split(')')[0].strip('(')) for session in self.sessions]
        for session in sessions_id:
            session_box = self.driver.find_elements(By.NAME, SESSION_TIME_NAME)[session-1]
            if session_box.get_attribute('disabled') is None:
                session_box.click()
                reserve_success = True

                self.wait_value(self.driver, By.ID, SESSION_TIME_DIV_ID)
                sessions = self.driver.find_element(By.ID, SESSION_TIME_DIV_ID).get_attribute('innerText')
                reserve_session = sessions.split('\n')[session-1]
                break
        
        # Submit the form
        self.driver.find_element(By.XPATH, BOOK_BUTTON).click()
        
        self.wait_alert(self.driver)
        self.handle_alert(self.driver)

        # Successfully booked
        self.wait_alert(self.driver)
        self.handle_alert(self.driver)

        time.sleep(30)
        return reserve_success, reserve_session

    
    def wait_value(self, driver, by_value, element_value, timeout=10):
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_value, element_value)))


    def wait_alert(self, driver):
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        

    def handle_alert(self, driver, accept=True):
        if accept:
            driver.switch_to.alert.accept()
        else:
            driver.switch_to.alert.dismiss()