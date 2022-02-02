'''

Webscraper for checking updates to websites with random time intervals between requests.
Browser doesn't appear onscreen or disrupt work.
It also sends you a telegram message when the desired phrase is found!

Created by Simon Drugan

Telegram bot guide:
https://medium.com/@mycodingblog/get-telegram-notification-when-python-script-finishes-running-a54f12822cdc
Credit: mycodingblog

You will have to download some imports too!

Completed as of 29/01/22

'''

# imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import threading
import random
import telegram
import sys

# main method
def WebScraperSiteX():
    
    # site you want to scrape
    web = "<insert website to scrape>"
    
    # local copy of webdriver
    ser = Service("<insert path to webdriver>")

    # keyword you are searching for on screen
    Phrase = "<insert phrase to check for>"
    
    # instantiating collections
    listOfLetters = []
    stringOfLetters = ''
    
    # starting webdriver options
    options = webdriver.ChromeOptions()
    
    # keeping the popup window unobtrusive
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1,1")
    options.add_argument("--window-position=4000,-35")
    
    # starting driver
    driver = webdriver.Chrome(options = options, service = ser)
    wait = WebDriverWait(driver, 20)
    
    # driver opening website
    driver.get(web)

    # saving site's html data
    html = driver.page_source
    
    # capturing desired data in a variable once it loads
    # must change the content after "contains" to the data you want to capture by
    # inspecting desired webpage
    elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'<insert html keyword>')]")))
    
    # converting captured data to readable text
    capturedText = elem.text
    
    # captured data in gamesAvailable is in the wrong form so these loops
    # convert it to a string
    for i in capturedText:
        listOfLetters.append(i)
    for i in range(len(listOfLetters)):
        stringOfLetters += listOfLetters[i-1]
        
    # checking if keyword stated earlier is in the captured data    
    if Phrase in stringOfLetters:
        
        # ouput success message to shell
        print("Phrase found!")
        
        # sends desired notification message to telegram method
        notifyReady("<insert telegram message>")
        
        # stops the program running
        # remove if you want the programme to keep running
        sys.exit(0)
    
    # shut the opened site upon completion
    driver.quit()

# decreases ease of detection as random request intervals
def randomWaitTime():
    
    # input min and max boundaries for interval times
    minWaitTimeInMinutes = 1
    maxWaitTimeInMinutes = 2
    
    # cleaner code and can change if wanted
    oneMillion = 1000000
    
    # creates random number in minues timesed by one million to that there
    # are not discrete int outputs (easy for a site to spot)
    randomNumber = random.randint(minWaitTimeInMinutes*oneMillion*
                                  60, maxWaitTimeInMinutes*oneMillion*60)
    
    # converting back to desired order of magnitude
    WAIT_TIME = randomNumber/oneMillion
    
    # printing is good indicator that the code is working
    print("new wait time", WAIT_TIME)
    
    # return the random number to method call
    return WAIT_TIME

def notifyReady(message):
    
    # add telegram bot token and chat id
    # telegram bot link is in the docstring
    token = '<add bot token>'
    chat_id ='<add chat id>'
    
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=message)

# starts ticket for looping programme
ticket = threading.Event()

while not ticket.wait(randomWaitTime()):
    
    # run main method
    WebScraperSiteX()

