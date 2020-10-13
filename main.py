# Date-Created: 7/28/2020
# Original Creator: Franklin
# Last Edited: 7/28/2020
# Current Editors: Franklin

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

@function closeNonSenseEnergySaverDialogBox(): Sometimes energy cap will load up some energy saver pop-up upon signing in and
it does not leave even if you traverse to an entirely different page. Hopefully, they don't introduce another of this kind so
that you don't have to implement another workaround just to close it but it isn't too bad if you do. If the dialog box ever
disappears for good you can remove the function call at the bottom or just leave it. It'll eventually timeout on its own anyway.

@functions tickboxes() && enterfields(): Energy cap will remember he settings you selected for any given report on a user to
user basis. The functions are written so that if someone, new or withstanding, would like to modify the code for their own
energy cap account it can account for freshly made or saved entries. That's why it clears entries and checks if the boxes
are ticked before proceeding.

@function mailit(): HTML is sick. Gmail doesn't natively support tables so the options you're left with is copy and pasting one
from google docs or using html to format the table into the email using pandas dataframes.

@param .format(df.to_html()): .format() takes a curly braced parameter inside of quotes and fills it in. In this case, it takes
the entire html formatting pandas spits out for the datatable and fills it in where {0} is.

@function cleanup(): Always make sure to quit out of the webdriver to save memory and also to just close out the web browser
the idea of this program is to make it run and leave no trace of it ever having been ran. It's simply more convenient to the end
user to not have to close out some dialog box.

@param BooleanHoliday: This is to save coworkers the headache of receiving an email on their break. Boolean Holiday also sounds
like a great band name.

Documentation End
"""

with open('config.json') as f:
    config = json.load(f)


driver = webdriver.Chrome("D:\\Documents\\chromedriver_win32\\chromedriver.exe")
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
            os.mkdir("C:/Users/Home/Desktop/BillOverDueErrorLogs/")
        except FileExistsError:
            print("It does exist, moving along...")
        method_name = 'exception_' + exceptionName
        method = getattr(self, method_name, lambda: 'Invalid')
        return method()

    def exception_IncorrectUrlException(self):
        path = "C:/Users/Home/Desktop/BillOverDueErrorLogs/IncorrectUrlException" + now.strftime("%m-%d-%Y-%I-%M-%S")
        driver.get_screenshot_as_file(path + ".png")
        errorLog = open(path + ".txt", "w+")
        errorLog.write("It seems we've run into an IncorrectUrlException \n \n")
        errorLog.write("This was the webpage you were sent to: " + driver.current_url + " \n")
        errorLog.write("Make sure your credentials don't need to be reset and that the url hasn't changed.")
        print("check the desktop, there should be a log folder on it")
        time.sleep(3)
        driver.quit()
        sys.exit()


    def exception_TimeoutException(self):
        path = "C:/Users/Home/Desktop/BillOverDueErrorLogs/TimeoutException" + now.strftime("%m-%d-%Y-%I-%M-%S")
        driver.get_screenshot_as_file(path + ".png")
        errorLog = open(path + ".txt", "w+")
        errorLog.write("It seems we've run into a TimeoutException trying to request the bill report url \n \n")
        errorLog.write("This was the webpage you were sent to: " + driver.current_url + " \n")
        errorLog.write("It's possible the url for the bill report is currently somewhere else or the page never loaded.")
        print("check the desktop, there should be a log folder on it")
        time.sleep(3)
        driver.quit()
        sys.exit()


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
