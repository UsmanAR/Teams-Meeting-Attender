from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import datetime
import requests
import csv
from threading import Timer 

   #####  ENTER VALUES  HERE ######
email_id=""
password=""
webhook=""
## SUBJECT NAMES SHOULD BE SAME AS IN THE TIMETABLE ## 
Positions={
        "PWP":13,
        "MAD":14,
        "PWP(Practical)":15,
        "ETI":16,
        "MGT":17,
        "WBP":18, 
        "EDP":19
    }
def getTimeTable():
    schedule=[]
    times=[]
    today=datetime.datetime.today()
    i=1
    timings=""
    with open('timetable.csv','r') as file:
        reader=csv.reader(file)
        times=next(reader)
        for row in reader:
            if today.strftime("%A").upper()==row[0]:
                schedule=row
                for sub in schedule[1:]:
                    if sub!="":
                        timings+=times[i]+" "
                    i+=1
    schedule=list(filter(None,schedule))
    timings=timings.replace('-', ' ').split(' ')
    timings=timings[:-1]
    if today.strftime("%A")=="Sunday":
        print("ITS WEEKEND")
    else:
        joinMeeting(schedule,today,timings)


def sendMessage(status,cancel,sub):
	t=datetime.datetime.today()
    if  cancel:
           message={
            "content":"Class  "+ str(sub)+ " has probably been cancelled  " 
            }
    else:
        if status:
            message={
            "content":"I've joined "+ str(sub)+ " class at " +  str(t.hour)+":"+str(t.minute) + " :)"
            }
        else:
            message={
            "content":"I've left " + str(sub)+ " class at " +  str(t.hour)+":"+str(t.minute) + " :)"
            }
    requests.post(webhook,data=message)

def joinMeeting(schedule,today,timings):
    options=webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    #options.add_argument("--disable-notifications")
    prefs = {"profile.default_content_setting_values.notifications" : 2,    
            "profile.default_content_setting_values.media_stream_mic": 2, 
            "profile.default_content_setting_values.media_stream_camera": 2,}
    options.add_experimental_option("prefs",prefs)
    browser=webdriver.Chrome(chrome_options=options,executable_path="chromedriver.exe")
    browser.get("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&rver=7.3.6963.0&wp=MBI_SSL&wreply=https%3a%2f%2fwww.microsoft.com%2fen-in%2fmicrosoft-teams%2flog-in&lc=16393&id=74335&aadredir=1")
    hang_up=(By.ID,"hangup-button")
    email_field= (By.ID, "i0116")
    password_field = (By.ID, "i0118")
    nextup = (By.ID, "idSIButton9")
    signin = (By.ID,"idSIButton9")
    allow=(By.ID,"idSIButton9")
    teams_init=(By.ID,"ShellSkypeTeams_link")
    ajp=(By.XPATH,"(//div[@class='stv-item-inner-container'])[position()=20]")
    search=(By.ID,"searchInputField")
    Teams=(By.ID,"app-bar-2a84919f-59d8-4441-a975-2a8c2643b741")
    join_in=(By.XPATH,"//button[@class='ts-sym ts-btn ts-btn-primary inset-border icons-call-jump-in ts-calling-join-button app-title-bar-button app-icons-fill-hover call-jump-in']")
    audio_video_btn=(By.XPATH,"//button[@class='ts-btn ts-btn-fluent ts-btn-fluent-secondary-alternate']")
    final_join=(By.XPATH,"//button[@class='join-btn ts-btn inset-border ts-btn-primary']")
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(signin)).click()
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(email_field)).send_keys(email_id)
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(nextup)).click()
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(password_field)).send_keys(password)
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(signin)).click()
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(allow)).click()
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(teams_init)).click()
    main_window = browser.current_window_handle
    browser.switch_to.window(browser.window_handles[1])
    while 1:
        today=datetime.datetime.today()
        if today.hour+today.minute/100>=float(timings[1]):
            timings=timings[2:]
            schedule.pop(1)
        else:
         if today.hour+today.minute/100>=float(timings[0]):
            present_sub=schedule[1]
            subject=schedule[1]
            current_position=Positions[present_sub]
            schedule.pop(1)
            present_sub=(By.XPATH,"(//div[@class='stv-item-inner-container'])[position()="+str(current_position)+"]")
            WebDriverWait(browser, 300).until(EC.element_to_be_clickable(present_sub)).click()
            time.sleep(5)
            try:
            	time.sleep(2)
                WebDriverWait(browser, 1800).until(EC.element_to_be_clickable(join_in)).click()
            except:
                timings=timings[2:]
                sendMessage(True,True,subject)
                WebDriverWait(browser, 30).until(EC.element_to_be_clickable(Teams)).click()
                WebDriverWait(browser, 30).until(EC.element_to_be_clickable(Teams)).click()
                continue
            WebDriverWait(browser, 30).until(EC.element_to_be_clickable(audio_video_btn)).click()
            WebDriverWait(browser, 30).until(EC.element_to_be_clickable(final_join)).click()
            sendMessage(True,False,subject)
            WebDriverWait(browser, 30).until(EC.element_to_be_clickable(Teams)).click()
            WebDriverWait(browser, 30).until(EC.element_to_be_clickable(Teams)).click()
            timings.pop(0)
            while 1:
                today=datetime.datetime.today() 
                if today.hour+today.minute/100>=float(timings[0]):
                    try:
                        WebDriverWait(browser, 30).until(EC.element_to_be_clickable(hang_up)).click()
                        sendMessage(False,False,subject)
                        timings.pop(0)
                        break
                    except:
                        sendMessage(False,False,subject)
                        timings.pop(0)
                        break
                else:
                    time.sleep(120)
         else:
            time.sleep(120)
        if len(timings)==0:
            print("Meetings Unavailable/Over... \nBot is shutting down...")
            exit()

getTimeTable()
