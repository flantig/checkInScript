# Date-Created: 7/28/2020
# Original Creator: Franklin
# Last Edited: 7/28/2020
# Current Editors: Franklin

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from datetime import datetime
import time
import os
import sys

"""
Documentation Start 

************************************************************************************************        
************************************************************************************************        
DO NOT upload this file to "The Manual" google doc without removing credentials, please follow the instructions listed in "The Manual"
************************************************************************************************    
************************************************************************************************ 

@general: Every single function and webdriver boilerplate use some kind of reactive programming. In other words,
before executing the majority of code it will wait until something either loads up or is available. This is due to
the non-instantaneous nature of the internet. If new code is implemented that requires data to load it is recommended
you use selenium's WebDriverWait(driver, timeout).until(element) functionality for web related events or set a manual
sleep timer if necessary like the following code block:

    timeout = 0
    while not os.path.exists('BL34C-Bills Overdue From Vendor - Excel Format.xlsx') and timeout != 30:
        timeout = timeout + 1
        time.sleep(1)           

@param webdriver: Allows you to use selenium to traverse your browser

@class generateExceptionReport(): If you want to add exception handling, please add it to this class. It acts just like a switch
statement and can be reused for any portion of the code that requires error handling. It outputs an error log file and a screenshot
of the page in the location the exception was raised. 

@json config.json: You're going to need to add the necessary information for your own login. If you have 2FA you're going to need to add your
browser's user profile. If you don't need 2FA, you can leave it as is.


Documentation End
"""

"""ToDo: Whenever I have class next, I'll actually add in the bit for the check in button"""

with open('config/config.json') as f:
    config = json.load(f)

if not config['userProfile'] == " ":
    options = webdriver.ChromeOptions()
    options.add_argument(config['userProfile'])
    driver = webdriver.Chrome(executable_path= config['webdriver'], chrome_options= options)
    driver.set_page_load_timeout(60)
else:
    driver = webdriver.Chrome(config['webdriver'])
    driver.set_page_load_timeout(60)


username= config['username']
password= config['password']
classname = config['class']
now = datetime.now()
date = now.strftime("%m-%d-%Y")


class IncorrectUrlException(Exception):
    pass

class generateExceptionReport(object):
    def generateExceptionReport(self, exceptionName):
        print("There has been an error, generating a log...")
        print("Creating an error log directory if it doesn't exist...")
        try:
            os.mkdir("C:/Users/Home/Desktop/ErrorLogs/")
        except FileExistsError:
            print("It does exist, moving along...")
        method_name = 'exception_' + exceptionName
        method = getattr(self, method_name, lambda: 'Invalid')
        return method()

def starter(username, password):
    timeout = 5
    print("It's running..")
    try:
        target = "https://templeu.instructure.com"
        driver.get(target)
        WebDriverWait(driver, timeout).until(EC.url_contains("https://fim.temple.edu/idp/") or EC.url_contains("https://templeu.instructure.com"))
        url = driver.current_url

    except TimeoutException:
        errorHandle = generateExceptionReport()
        errorHandle.generateExceptionReport("TimeoutException")

    if ("https://fim.temple.edu/idp/" in url):
        signin(username, password)

def signin(username, password):
    timeout = 5

    usernameField = driver.find_element_by_css_selector('#username')
    usernameField.clear()
    usernameField.send_keys(username)

    usernameField = driver.find_element_by_css_selector('#password')
    usernameField.clear()
    usernameField.send_keys(password)
    try:
        loginbutton = EC.presence_of_element_located((By.XPATH,"//*[@id='login-container']/div[1]/form/div[6]/button"))
        WebDriverWait(driver, timeout).until(loginbutton)
        loginbutton = driver.find_element_by_xpath("//*[@id='login-container']/div[1]/form/div[6]/button")
        loginbutton.click()
    except TimeoutException:
        errorHandle = generateExceptionReport()
        errorHandle.generateExceptionReport("TimeoutException")



def checkin(className):
    timeout = 5
    target = className
    driver.get(target)
    try:
        attendance = EC.presence_of_element_located((By.XPATH,"//*[@id='section-tabs']/li[11]/a"))
        WebDriverWait(driver, timeout).until(attendance)
        attendance = driver.find_element_by_xpath("//*[@id='section-tabs']/li[11]/a")
        attendance.click()
    except TimeoutException:
        errorHandle = generateExceptionReport()
        errorHandle.generateExceptionReport("TimeoutException")


    windows = driver.window_handles
    print("opened windows length: ", len(windows))
    driver.switch_to.window(driver.window_handles[1])
    url = driver.current_url
    print("Current Page Title is : %s" %driver.title)
    if "login/oauth2/confirm" in url:
        authorize = EC.presence_of_element_located((By.XPATH,"//*[@id='oauth2_accept_form']/div/input"))
        WebDriverWait(driver, timeout).until(authorize)
        authorize = driver.find_element_by_xpath("//*[@id='oauth2_accept_form']/div/input")
        authorize.click()




print("It's running..")

starter(username, password)
checkin(classname)
