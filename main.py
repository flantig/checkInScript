# Date-Created: 10/13/2020
# Original Creator: Franklin
# Last Edited: 10/13/2020
# Current Editors: Franklin

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from pathlib import Path
import json
from datetime import datetime
import time
import os
import sys

"""
Documentation Start 

************************************************************************************************        
************************************************************************************************        
DO NOT SHARE YOUR CONFIG.JSON WITH ANYONE YOU SAUERKRAUT LOOKING CRETIN
************************************************************************************************    
************************************************************************************************ 

@general: Every single function and webdriver boilerplate use some kind of reactive programming. In other words,
before executing the majority of code it will wait until something either loads up or is available. This is due to
the non-instantaneous nature of the internet. If new code is implemented that requires data to load it is recommended
you use selenium's WebDriverWait(driver, timeout).until(element) functionality for web related events or set a manual
sleep timer if necessary like the following code block:

    timeout = 0
    while not os.path.exists('config.json') and timeout != 30:
        timeout = timeout + 1
        time.sleep(1)           

@param webdriver: Allows you to use selenium to traverse your browser

@class generateExceptionReport(): If you want to add exception handling, please refer to this class. It acts just like a switch
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
        home = str(Path.home())
        try:
            os.mkdir(home + "\ErrorLogs\\")
        except FileExistsError:
            print("It does exist, moving along...")
        method_name = 'exception_' + exceptionName
        method = getattr(self, method_name, lambda: 'Invalid')
        return method()

    def exception_NoSuchElementException(self):
        home = str(Path.home())
        path = home + "\ErrorLogs\IncorrectUrlException" + now.strftime("%m-%d-%Y-%I-%M-%S")
        driver.get_screenshot_as_file(path + ".png")
        errorLog = open(path + ".txt", "w+")
        errorLog.write("It seems we've run into a NoSuchElementException \n \n")
        errorLog.write("If you got here, it probably means that we couldn't find a checkin button.\n")
        errorLog.write("So you either already checked in or the professor hasn't actually put up attendance yet.")
        print("check the desktop, there should be a log folder on it at: " + path)
        time.sleep(5)
        driver.quit()
        sys.exit()

    def exception_TimeoutException(self):
        home = str(Path.home())
        path = home + "/ErrorLogs/IncorrectUrlException" + now.strftime("%m-%d-%Y-%I-%M-%S")
        driver.get_screenshot_as_file(path + ".png")
        errorLog = open(path + ".txt", "w+")
        errorLog.write("It seems we've run into a TimeoutException \n \n")
        errorLog.write("Looks like the browser took too long to load the page.\n")
        errorLog.write("Either the page broke or the connection is unusually slow.")
        print("check the desktop, there should be a log folder on it at: " + path)
        time.sleep(5)
        driver.quit()
        sys.exit()

def starter(username, password):
    timeout = 5
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
    try:
        checkin = EC.presence_of_element_located((By.XPATH,"/html/body/div/div[1]/div[2]"))
        WebDriverWait(driver, timeout).until(checkin)
    except TimeoutException:
        errorHandle = generateExceptionReport()
        errorHandle.generateExceptionReport("TimeoutException")

    try:
        checkin = driver.find_element_by_xpath("//*[@id='student_check_in']")
        checkin.click()
        driver.quit()
    except NoSuchElementException:
        errorHandle = generateExceptionReport()
        errorHandle.generateExceptionReport("NoSuchElementException")
        driver.quit()




print("It's running..")

starter(username, password)
checkin(classname)