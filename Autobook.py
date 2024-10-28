# Import the required modules
# from selenium import webdriver #deprecated
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from discordwebhook import Discord
from webdriver_auto_update.chrome_app_utils import ChromeAppUtils
from webdriver_auto_update.webdriver_manager import WebDriverManager
import credentials
import room_id as room_ids
import math
import time
import random
import argparse
import platform
import os
import sys
import stat
import shutil

DISCORD_WEBHOOK = 'https://discord.com/api/webhooks/1147262918199611484/mQyvGE3rE1MKGXpFLjKYKicyjyeV_Q7tvq3BVp9TdenHOQSk2qMohPGnHV5tiAoIA90l'

username = password = ''
room_id = None
date = day = month = year = discord_day = discord_month = ''
discord_end_time=0
name=''

def initialize_parser(parser):
    parser.add_argument('-d', '--date', type=str, nargs='+', required=True,
                        help='Date of the booking. Typing the day (ex. Monday) will book the nearest next occurrence that isn\'t today.\
                            You can also type the calendar date, ie. Aug 23')

    parser.add_argument('-r', '--room', type=str, required=True,
                        help='The room number you want to book. Can also book subrooms, ie. 324A')

    parser.add_argument('-t', '--time', type=int, required=True,
                        help='The start time of your desired booking time in military hours, ie. 1800 = 6:00 PM')

    parser.add_argument('-u', '--username', type=str, nargs='+', required=False,
                        help='Username for Carleton Central. This will take precedence over credentials.py username')

    parser.add_argument('-p', '--password', type=str, required=False,
                        help='Password for Carleton Central. This will take precedence over credentials.py password')

    parser.add_argument('--duration', type=int, default=180, required=False,
                        help='Desired duration of your booking in minutes. 30 minute increments; Max 180 minutes. Default 180 minutes')

    parser.add_argument('--headless', action='store_true', default=False, required=False,
                        help='Runs the program in headless mode (Does not open the browser). Default is false')

def parse_args(args):
    global username, password, room_id

    args.date = ' '.join(args.date)
    args.room=args.room.upper()
    room_id = room_ids.room_ids[args.room]

    if args.username is not None and args.password is not None:
        username, password = args.username, args.password
    else:
        username, password = credentials.username, credentials.password
    if not username or not password:
        sys.exit("\nPLEASE ADD YOUR CREDENTIALS IN CREDENTIALS.PY OR AS COMMAND LINE ARGUMENTS\n")


#print("Platform: " + platform.system())
#print("Argument values:")
#print("Date: " + args.date)
#print("Room: " + args.room)
#print("Time: " + str(args.time))
#print("Username: " + args.user)
#print("Password: " + args.password)
#print("Duration: " + str(args.duration))
#print("Headless: " + str(args.headless))
#print("Room ID: " + str(room_id))

class Browser:
    browser, service, options = None, None, Options()
    
    def __init__(self, driver: str):
        self.service = Service(driver)
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("--log-level=1")
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

    #Closes the browser
#    def take_screenshot(self): 
#        self.browser.save_screenshot('screenshot.png')

    #Adds input [text] to element [value]
    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(0.5)
        
    #Clicks button found by [by] with identifier [value]
    def click_button(self, by: By, value: str): 
        button = self.browser.find_element(by=by, value=value)
        button.click()
        time.sleep(1)
        
    #Gets the unix timestamp for the date and returns it
    def get_unix_timestamp(self) -> str:
        global date, day, month, year, discord_day
        day_map = {
            "SUN" : "saturday",
            "SUNDAY" : "saturday",

            "MON" : "sunday",
            "MONDAY" : "sunday",

            "TUE" : "monday",
            "TUES" : "monday",
            "TUESDAY" : "monday",

            "WED" : "tuesday",
            "WEDNESDAY" : "tuesday",

            "THU" : "wednesday",
            "THURS" : "wednesday",
            "THURSDAY" : "wednesday",

            "FRI" : "thursday",
            "FRIDAY" : "thursday",

            "SAT" : "friday",
            "SATURDAY" : "friday"
        }
        discord_day_map = {
            "SUN" : "Sunday",
            "SUNDAY" : "Sunday",

            "MON" : "Monday",
            "MONDAY" : "Monday",

            "TUE" : "Tuesday",
            "TUES" : "Tuesday",
            "TUESDAY" : "Tuesday",

            "WED" : "Wednesday",
            "WEDNESDAY" : "Wednesday",

            "THU" : "Thursday",
            "THURS" : "Thursday",
            "THURSDAY" : "Thursday",

            "FRI" : "Friday",
            "FRIDAY" : "Friday",

            "SAT" : "Saturday",
            "SATURDAY" : "Saturday"
        }
        # date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
        # day=date[0]
        # month=date[1]
        # year=date[2]

        if args.date.upper() in day_map:
            weekday = day_map[args.date.upper()]
            browser.open_page(f'https://www.unixtimesta.mp/{weekday}')
            date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
            day=date[0]
            month=date[1]
            year=date[2]
            timestamp = str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
            browser.open_page('https://www.unixtimesta.mp/'+timestamp)
            discord_day = discord_day_map[args.date.upper()]
            return timestamp
        else:
            browser.open_page('https://www.unixtimesta.mp/' + args.date.replace(" ", ""))
            date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
            day=date[0]
            month=date[1]
            year=date[2]
            discord_day = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[0].split(" ")[-1]
            return self.browser.current_url.replace("https://www.unixtimesta.mp/", "")

        # match args.date.upper():
        #     case "SUNDAY" | "SUN":
        #         #browser.open_page('https://www.unixtimesta.mp/saturday')
                
        #         return timestamp
        #     case "MONDAY" | "MON":
        #         #browser.open_page('https://www.unixtimesta.mp/sunday')
        #         discord_day='Monday'
        #         return timestamp
        #     case "TUESDAY" | "TUE" | "TUES":
        #         #browser.open_page('https://www.unixtimesta.mp/monday')
        #         discord_day='Tuesday'
        #         return timestamp
        #     case "WEDNESDAY" | "WED":
        #         #browser.open_page('https://www.unixtimesta.mp/tuesday')
        #         discord_day='Wednesday'
        #         return timestamp
        #     case "THURSDAY" | "THU" | "THURS":
        #         #browser.open_page('https://www.unixtimesta.mp/wednesday')
        #         discord_day='Thursday'
        #         return timestamp
        #     case "FRIDAY" | "FRI":
        #         #browser.open_page('https://www.unixtimesta.mp/thursday')
        #         discord_day='Friday'
        #         return timestamp
        #     case "SATURDAY" | "SAT":
        #         #browser.open_page('https://www.unixtimesta.mp/friday')
        #         discord_day='Saturday'
        #         return timestamp
        #     case _:
        #         discord_day = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[0].split(" ")[-1]
        #         return self.browser.current_url.replace("https://www.unixtimesta.mp/", "")
            
    #Login to the booking site using the username and password found in credentials.py
    def login_carleton(self, username: str, password: str):
        browser.open_page('https://brightspace.carleton.ca/d2l/home')
        self.add_input(by=By.ID, value='userNameInput', text=username)
        self.add_input(by=By.ID, value='passwordInput', text=password)
        self.click_button(by=By.ID, value='submitButton')
        time.sleep(3)
        if self.browser.find_elements(by=By.ID, value='loginForm'):
            raise Exception()
    
    #Login to the booking site using the username and password found in credentials.py
    def get_date(self):
        global date, day, month, year, discord_end_time, discord_month
        day=date[0].zfill(2)
        discord_month = month
        match month.upper():
            case "JANUARY" :
                month='01'
            case "FEBRUARY" :
                month='02'
            case "MARCH" :
                month='03'
            case "APRIL" :
                month='04'
            case "MAY" :
                month='05'
            case "JUNE" :
                month='06'
            case "JULY" :
                month='07'
            case "AUGUST" :
                month='08'
            case "SEPTEMBER" :
                month='09'
            case "OCTOBER" :
                month='10'
            case "NOVEMBER" :
                month='11'
            case "DECEMBER" :
                month='12'
            case _:
                sys.exit("SOMETHING WENT WRING WITH MONTH MANIPULATION")
        date = f'{year}-{month}-{day}'
        #Calculate end time in military hours
        if (args.duration/60).is_integer() == True:
            discord_end_time = int(args.time + (args.duration/60 * 100))
        elif int(args.time + (math.floor(args.duration/60) * 100 + 30)) % 100 == 60:
            discord_end_time = int(args.time + (math.floor(args.duration/60) * 100 + 30)) - 60 + 100
        else:
            discord_end_time = int(args.time + (math.floor(args.duration/60) * 100 + 30))
    #Books the room
    def book_room(self, unix_timestamp: str):
        global name

        browser.open_page('https://carletonu.libcal.com/r/accessible/availability?lid=2986&zone=0&gid=0&capacity=2&space=')

        self.click_button(by=By.ID, value='date') #Select dropdown menu
        select = Select(self.browser.find_element(by=By.ID,value='date'))
        select.select_by_value(date)
        self.click_button(by=By.ID, value='s-lc-submit-filters') #Select dropdown menu
        time.sleep(2)

        #Calculate seconds of time to add to 12:00AM
        if (args.time/100).is_integer() == True:
            start = int(args.time/100 * 60) * 60
        else:
            start = (math.floor(args.time/100) * 60 + 30) * 60
        current_timestamp = int(unix_timestamp) + start
        end_timestamp = current_timestamp + args.duration * 60
        while(current_timestamp != end_timestamp):
            self.click_button(by=By.ID, value=f's{room_id}_0_{current_timestamp}')
            current_timestamp += 1800

        self.click_button(by=By.ID, value='s-lc-submit-times') #Submit Times
        self.click_button(by=By.ID, value='terms_accept') #Continue

        name = self.browser.find_element(by=By.CLASS_NAME, value='s-lc-session-aware-link').text.split()[:2] #Click on the first 'Book' button

        self.click_button(by=By.ID, value='btn-form-submit') #Submit my Booking
        if self.browser.find_elements(by=By.CLASS_NAME, value='jquery-notification-error'):
            raise Exception()
        time.sleep(1)


# Main Function
if __name__ == '__main__':
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='An automated booking script for Carleton Library rooms')

    discord = Discord(url=DISCORD_WEBHOOK)

    # Initialize argparse
    initialize_parser(parser)

    # Parse the args
    args = parser.parse_args()
    parse_args(args)
    
    # Target directory to store chromedriver
    if platform.system() == "Windows":
        driver_directory = 'drivers\windows'
    elif platform.system() == "Darwin":
        driver_directory = 'drivers/mac'
    elif platform.system() == "Linux":
        driver_directory = 'drivers/linux'

    # Create an instance of WebdriverAutoUpdate
    driver_manager = WebDriverManager(driver_directory)

    # Call the main method to manage chromedriver
    print("\n---ENSURING LATEST VERSION OF CHROMEDRIVER---\n")
    driver_manager.main()
    time.sleep(2)

    #Support for different architectures
    if platform.system() == "Windows":
        try:
            shutil.move("drivers\windows\chromedriver-win64\chromedriver.exe", "drivers\windows\chromedriver.exe")
            try:
                shutil.rmtree('drivers\windows\chromedriver-win64')
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        except:
            pass
        os.chmod('drivers\windows\chromedriver.exe', stat.S_IRWXU)
        browser = Browser('drivers\windows\chromedriver.exe')
    elif platform.system() == "Darwin":
        try:
            shutil.move("drivers/mac/chromedriver-mac-arm64/chromedriver", "drivers/mac/chromedriver")
            try:
                shutil.rmtree('drivers/mac/chromedriver-mac-arm64')
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        except:
            pass
        os.chmod('drivers/mac/chromedriver', stat.S_IRWXU)
        browser = Browser('drivers/mac/chromedriver')
    elif platform.system() == "Linux":
        try:
            shutil.move("drivers/linux/chromedriver-linux64/chromedriver", "drivers/linux/chromedriver")
            try:
                shutil.rmtree('drivers/linux/chromedriver-linux64')
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        except:
            pass
        os.chmod('drivers/linux/chromedriver', stat.S_IRWXU)
        browser = Browser('drivers/linux/chromedriver')

    print("\n-------GETTING UNIX TIMESTAMP AND DATE-------\n")
    try:
        unix_timestamp = str(int(browser.get_unix_timestamp()) + 14400)
        browser.get_date()
        print("-------------------SUCCESS-------------------\n\n\n")
    except:
        print("-----------FAILED TO GET TIMESTAMP-----------\n")
        print("---------------EXITING PROGRAM---------------\n\n")
        exit()

    print("\n-------LOGGING IN TO CARLETON CENTRAL--------\n")
    try:
        browser.login_carleton(username, password)
        print("-------------------SUCCESS-------------------\n\n\n")
    except:
        print("---------------FAILED TO LOGIN---------------\n")
        print("-----------PLEASE CHECK CREDENTIALS----------\n")
        print("---------------EXITING PROGRAM---------------\n\n")
        exit()

    print("-----------ATTEMPTING TO BOOK ROOM-----------\n")
    try:
        browser.book_room(unix_timestamp)
        print("-------------------SUCCESS-------------------\n\n\n")
    except:
        print("-------------FAILED TO BOOK ROOM-------------\n")
        print("------ROOM MIGHT BE UNAVAILABLE TO BOOK------")
        print("-------OR DESIRED TIMESLOT UNAVAILABLE-------")
        print("--------OR EXCEEDED DAILY 6 HOUR LIMIT-------\n")
        print("---------------EXITING PROGRAM---------------\n\n")
        exit()
    try:
        print("--------------POSTING TO DISCORD-------------\n")
        time.sleep(random.randint(0,10)) #Sleep to circumvent discord rate limit
        start_time = str(args.time).zfill(4)
        end_time = str(discord_end_time).zfill(4)
        discord.post(
            username=f'{name[0]} {name[1]}',
            embeds=[
            {
                "title": "Carleton Libary Room Booking",
                "fields": [
                    {"name": "Date", "value": f'{discord_day}, {day} {discord_month} {year}', "inline": True},
                    {"name": "Room", "value": f'{args.room}', "inline": True},
                    {"name": "Time", "value": f'{start_time[:2]}:{start_time[2:]} -> {end_time[:2]}:{end_time[2:]}'},
                ],
            }
            ],
        )
        print("-------------------SUCCESS-------------------\n\n\n")
    except:
        print("----------FAILED TO POST TO DISCORD----------\n")

    browser.close_browser
