# Import the required modules
# from selenium import webdriver #deprecated
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import credentials
import math
import time
import argparse
import platform
import os
import stat

# Instantiate the parser
parser = argparse.ArgumentParser(description='An automated booking script for Carleton Library rooms')

parser.add_argument('-d', '--date', type=str, nargs='+', required=True,
                    help='Date of the booking. Typing the day (ex. Monday) will book the nearest next occurrence that isn\'t today.\
                          You can also type the calendar date, ie. Aug 23')

parser.add_argument('-r', '--room', type=str, required=True,
                    help='The room number you want to book. Can also book subrooms, ie. 324A')

parser.add_argument('-t', '--time', type=int, required=True,
                    help='The start time of your desired booking time in military hours, ie. 1800 = 6:00 PM')

parser.add_argument('-u', '--username', type=str, required=False,
                    help='Username for MC1 login. This will take precedence over credentials.py username')

parser.add_argument('-p', '--password', type=str, required=False,
                    help='Password for MC1 login. This will take precedence over credentials.py password')

parser.add_argument('--duration', type=int, default=180, required=False,
                    help='Desired duration of your booking in minutes. 30 minute increments; Max 180 minutes. Default 180 minutes')

parser.add_argument('--headless', action='store_true', default=False, required=False,
                    help='Runs the program in headless mode (Does not open the browser). Default is false')

args = parser.parse_args()
args.date = ' '.join(args.date)
if args.username is not None and args.password is not None:
    username, password = args.username, args.password
else:
    username, password = credentials.username, credentials.password

#print("Platform: " + platform.system())
#print("Argument values:")
#print("Date: " + args.date)
#print("Room: " + args.room)
#print("Time: " + str(args.time))
#print("Username: " + args.user)
#print("Password: " + args.password)
#print("Duration: " + str(args.duration))
#print("Headless: " + str(args.headless))

class Browser:
    browser, service, options = None, None, Options()
    
    def __init__(self, driver: str):
        self.service = Service(driver)
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if args.headless == True:
            self.options.add_argument("--headless=new")
        self.browser = webdriver.Chrome(service=self.service, options=self.options)
        #self.browser = webdriver.Chrome(service=self.service)

    #Opens the desired page to [url]
    def open_page(self, url: str):
        self.browser.get(url)

    #Closes the browser
    def close_browser(self): 
        self.browser.close()

    #Adds input [text] to element [value]
    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(1)
        
    #Clicks button found by [by] with identifier [value]
    def click_button(self, by: By, value: str): 
        button = self.browser.find_element(by=by, value=value)
        button.click()
        time.sleep(1)
        
    #Gets the unix timestamp for the date and returns it
    def get_unix_timestamp(self) -> str:
        match args.date.upper():
            case "SUNDAY" | "SUN":
                browser.open_page('https://www.unixtimesta.mp/saturday')
                time.sleep(3)
                return str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
            case "MONDAY" | "MON":
                browser.open_page('https://www.unixtimesta.mp/sunday')
                time.sleep(3)
                return str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
            case "TUESDAY" | "TUE" | "TUES":
                browser.open_page('https://www.unixtimesta.mp/monday')
                time.sleep(3)
                return str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
            case "WEDNESDAY" | "WED":
                browser.open_page('https://www.unixtimesta.mp/tuesday')
                time.sleep(3)
                return str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
            case "THURSDAY" | "THU" | "THURS":
                browser.open_page('https://www.unixtimesta.mp/wednesday')
                time.sleep(3)
                return str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
            case "FRIDAY" | "FRI":
                browser.open_page('https://www.unixtimesta.mp/thursday')
                time.sleep(3)
                return str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
            case "SATURDAY" | "SAT":
                browser.open_page('https://www.unixtimesta.mp/friday')
                time.sleep(3)
                return str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
            case _:
                browser.open_page('https://www.unixtimesta.mp/' + args.date.replace(" ", ""))
                time.sleep(3)
                return self.browser.current_url.replace("https://www.unixtimesta.mp/", "")

    #Login to the booking site using the username and password found in credentials.py
    def login_booking_carleton(self, username: str, password: str):
        browser.open_page('https://booking.carleton.ca/')
        time.sleep(3)
        self.click_button(by=By.ID, value='spanLogin')
        self.add_input(by=By.ID, value='txtUsername', text=username)
        self.add_input(by=By.ID, value='txtPassword', text=password)
        self.click_button(by=By.ID, value='btnLogin')
        time.sleep(4)
        if self.browser.find_elements(by=By.ID, value='spanLogin'):
            raise Exception()
        browser.open_page('https://booking.carleton.ca/index.php?p=BookRoom&r=1')
        time.sleep(3)

    #Books the room
    def book_room(self, room: str, unix_timestamp: str):
        self.add_input(by=By.ID, value='listSearch', text=room) #Search for the room
        time.sleep(1)
        self.click_button(by=By.CLASS_NAME, value='SearchHighlight') #Select the room

        #Choose desired duration
        self.click_button(by=By.ID, value='cboDuration') #Select dropdown menu
        select = Select(self.browser.find_element(by=By.ID,value='cboDuration'))
        #select.select_by_visible_text('03:00')
        select.select_by_value(str(args.duration))
        time.sleep(1)

        #Select start time
        if (args.time/100).is_integer() == True:
            start = int(args.time/100 * 60)
        else:
            start = math.floor(args.time/100) * 60 + 30
        self.click_button(by=By.ID, value='cboStartTime') #Select dropdown menu
        select = Select(self.browser.find_element(by=By.ID,value='cboStartTime'))
        select.select_by_value(str(start))

        #Select end time
        self.click_button(by=By.ID, value='cboEndTime') #Select dropdown menu
        select = Select(self.browser.find_element(by=By.ID,value='cboEndTime'))
        select.select_by_value(str(start + args.duration))

        #Verify calendar button
        self.click_button(by=By.ID, value='btnAnyDate')
        time.sleep(1)

        #Click on calendar
        self.click_button(by=By.ID, value='day' + unix_timestamp) #Select the date
        xpath = '//*[@id="roomavailability"]/div/div/div[2]/table/tbody/tr[1]/td[2]/input'
        self.click_button(by=By.XPATH, value=xpath) #Click on the first 'Book' button

        #Booking confirmation page
        self.click_button(by=By.ID, value='btnConfirm')
        self.click_button(by=By.ID, value='btnOK')
        time.sleep(1)
        self.click_button(by=By.ID, value='btnOK')
        time.sleep(3)

# Main Function
if __name__ == '__main__':
    #Support for different architectures
    if platform.system() == "Windows":
        browser = Browser('drivers\chromedriver.exe')
        os.chmod('drivers\chromedriver.exe', stat.stat.S_IRWXU)
    elif platform.system() == "Darwin":
        browser = Browser('drivers/chromedriver_mac')
        os.chmod('drivers\chromedriver_mac', stat.stat.S_IRWXU)
    elif platform.system() == "Linux":
        browser = Browser('drivers/chromedriver_linux')
        os.chmod('drivers/chromedriver_linux', stat.stat.S_IRWXU)

    print("\n-------GETTING UNIX TIMESTAMP FOR DATE-------\n")
    try:
        unix_timestamp = browser.get_unix_timestamp()
        print("-------------------SUCCESS-------------------\n\n\n")
    except:
        print("-----------FAILED TO GET TIMESTAMP-----------\n")
        print("---------------EXITING PROGRAM---------------\n\n")
        exit()

    print("-------LOGGING INTO BOOKING.CARLETON.CA------\n")
    try:
        browser.login_booking_carleton(username, password)
        print("-------------------SUCCESS-------------------\n\n\n")
    except:
        print("---------------FAILED TO LOGIN---------------")
        print("-----------CHECK YOUR CREDENTIALS------------\n")
        print("---------------EXITING PROGRAM---------------\n\n")
        exit()

    print("-----------ATTEMPTING TO BOOK ROOM-----------\n")
    try:
        browser.book_room(args.room, unix_timestamp)
        print("-------------------SUCCESS-------------------\n\n\n")
        print("See your bookings here: https://booking.carleton.ca/index.php?p=MyBookings&r=1\n")
    except:
        print("-------------FAILED TO BOOK ROOM-------------\n")
        print("------ROOM MIGHT BE UNAVAILABLE TO BOOK------")
        print("-------OR DESIRED TIMESLOT UNAVAILABLE-------\n")
        print("---------------EXITING PROGRAM---------------\n\n")
        exit()
       
    browser.close_browser
