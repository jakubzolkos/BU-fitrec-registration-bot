#!/usr/bin/env python3

from dateutil.relativedelta import relativedelta
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import datetime as dt
import sys
import os
import shutil

def access_website(username, password, phone, workout_slot, workout_date):
    ''' Login to BU website and register for the workout '''

    driver.get("https://myfitrec.bu.edu/wbwsc/webtrac.wsc/splash.html?interfaceparameter=2&ccode=bu-login")
    driver.find_element_by_link_text("LOG IN WITH BU.EDU EMAIL").click()
    driver.find_element_by_id('j_username').send_keys(username)
    driver.find_element_by_id('j_password').send_keys(password)
    driver.find_element_by_class_name('input-submit').click()
    driver.find_element_by_css_selector('.btn.blue').click()
    time.sleep(1)
    driver.find_elements_by_css_selector('.button.cart-button.cart-button--state-icon.cart-button--icon-calendar.processed')[workout_slot[1]].click()
    links = driver.find_elements_by_css_selector('.block.button.multi-select.block-status.success.processed')
    hrefs = [element.get_attribute('href') for element in links]
    button_available = [href for href in hrefs if workout_date in href]
    
    if len(button_available) == 0:
        driver.close()
        access_website(username, password, phone, workout_slot, workout_date)
    else:
        links[hrefs.index(button_available[0])].click()
        time.sleep(1)
        driver.find_element_by_css_selector(".websearch_multiselect_buttonaddtocart.button.processed.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only").click()
        driver.find_element_by_css_selector(".checkbox.logical.valid").click()
        driver.find_element_by_id("processingprompts_buttoncontinue").click()
        driver.find_element_by_id("webcart_buttoncheckout").click()
        driver.find_element_by_id("webcheckout_billphone").send_keys(phone)
        driver.find_element_by_id("webcheckout_buttoncontinue").click()
        driver.close()
        
        return "Registration Successful"
    
    
def credentials():
    ''' Returns credentials for BU login website - INPUT YOUR CREDENTIALS BELOW '''

    username = ''
    password = ''
    phone = ''
    return username, password, phone

def workout_info():
    ''' Return the dates of first workout, ending date, and a list of tuples containing weekdays 
    and corresponding workout hours mapped to numbers '''

    first_workout = [2021, 7, 21] 
    ending_date = [2022, 5, 1]   

    dates = {
        'Friday': '1:00', 
        'Sunday': '1:00'
    }

    map_hours = {'7:00': 0, '9:00': 1, '11:00': 2, '1:00': 3, '3:00': 4, '5:00': 5}
    map_days = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    workout_slots =  list(zip(list(map(map_days.get, dates.keys())), list(map(map_hours.get, dates.values()))))
    
    return first_workout, ending_date, workout_slots

def workout_records(starting_date, ending_date, workout_info):
    ''' Creates a list containing strings with all the workout dates based on workout_info output '''

    weekdays = [day for (day, hour) in workout_info]
    workout = dt.datetime(*starting_date)
    workout_dates = []
    
    while workout < dt.datetime(*ending_date):
        if workout.weekday() in weekdays:
            workout_dates.append(f'{workout.strftime("%m/%d/%Y")}')
        else:
            pass
        
        workout += relativedelta(days = 1)
    
    return workout_dates

if __name__ == "__main__":
    
    CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
                             
    username, password, phone = credentials()
    first_workout, ending_date, workout_slots = workout_info()
    workout_dates = workout_records(first_workout, ending_date, workout_slots)

    # Adjust the list to current date - delete past days that are still on the list
    workout_dates = [date for date in workout_dates if dt.datetime.strptime(date, '%m/%d/%Y') >= dt.datetime.now()]
 
    # Run the program
    while len(workout_dates) != 0:
        for slot in workout_slots:
            while True:
                try:
                    driver = webdriver.Chrome(executable_path = CHROMEDRIVER_PATH, options = chrome_options)
                    STATUS = access_website(username, password, phone, slot, workout_dates[0])
                    if STATUS == "Registration Successful":
                        workout_dates.pop(0)
                        break
                except Exception:
                    continue

    
    



   
    