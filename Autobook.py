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
from enum import Enum
import credentials
import room_id as room_ids
import time
import random
import argparse
import platform
import os
import sys
import stat
import shutil

class Status(Enum):
    SUCCESS = 0
    ERROR = 1
    INVALID_ROOM = 2
    NO_CREDENTIALS = 3


def exit_program(message, code):
    print(message, file=sys.stderr)  # Print message to stderr
    sys.exit(code)

DISCORD_WEBHOOK = ''
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
    global username, password, room_id, DISCORD_WEBHOOK

    args.date = ' '.join(args.date)
    args.room=args.room.upper()

    if credentials.DISCORD_WEBHOOK:
        DISCORD_WEBHOOK = credentials.DISCORD_WEBHOOK
    
    if args.room not in room_ids.room_ids:
        message = "\nROOM DOES NOT EXIST. PLEASE CHOOSE A DIFFERENT ROOM\n"
        exit_program(message, Status.INVALID_ROOM.value)
    else:
        room_id = room_ids.room_ids[args.room]

    if args.username is not None and args.password is not None:
        username, password = args.username, args.password
    else:
        username, password = credentials.username, credentials.password
    if not username or not password:
        message = "\nPLEASE ADD YOUR CREDENTIALS IN CREDENTIALS.PY OR AS COMMAND LINE ARGUMENTS\n"
        exit_program(message, Status.NO_CREDENTIALS.value)

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

    # Opens the desired page to [url]
    def open_page(self, url: str):
        self.browser.get(url)

    # Closes the browser
    def close_browser(self): 
        self.browser.close()

    # Takes a screenshot
    #def take_screenshot(self): 
    #    self.browser.save_screenshot('screenshot.png')

    # Adds input [text] to element [value]
    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(0.5)
        
    # Clicks button found by [by] with identifier [value]
    def click_button(self, by: By, value: str): 
        button = self.browser.find_element(by=by, value=value)
        button.click()
        time.sleep(1)

    '''
    Gets the unix timestamp for the date and returns it (12:00AM EST)
    The day is mapped to the previous day because the unix timestamp website will only reliably get the next week when fed the previous 'day'.
    Therefore if given a weekday, add 29 hours in seconds to the timestamp. 24 hours (to make up for the difference in mapped time) and 5 hours (to make up the UTC -> EST difference)
    If given a specific date, only add 5 hours in seconds to make up for the time zone difference
    '''
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

        if args.date.upper() in day_map:
            weekday = day_map[args.date.upper()]
            browser.open_page(f'https://www.unixtimesta.mp/{weekday}')
            timestamp = str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 104400)
            browser.open_page('https://www.unixtimesta.mp/'+timestamp)
            discord_day = discord_day_map[args.date.upper()]
        else:
            browser.open_page('https://www.unixtimesta.mp/' + args.date.replace(" ", ""))
            discord_day = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[0].split(" ")[-1]
            timestamp = str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 18000)

        date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
        day=date[0]
        month=date[1]
        year=date[2]
        return timestamp
            
    # Login to the booking site using the username and password found in credentials.py
    def login_carleton(self, username: str, password: str):
        browser.open_page('https://brightspace.carleton.ca/d2l/home')
        self.add_input(by=By.ID, value='userNameInput', text=username)
        self.add_input(by=By.ID, value='passwordInput', text=password)
        self.click_button(by=By.ID, value='submitButton')
        time.sleep(3)
        if self.browser.find_elements(by=By.ID, value='loginForm'):
            raise Exception()
    
    # Login to the booking site using the username and password found in credentials.py
    def get_date(self):
        global date, day, month, year, discord_end_time, discord_month
        day=date[0].zfill(2)
        discord_month = month
        month_map = {
            'JANUARY': '01',
            'FEBRUARY': '02',
            'MARCH': '03',
            'APRIL': '04',
            'MAY': '05',
            'JUNE': '06',
            'JULY': '07',
            'AUGUST': '08',
            'SEPTEMBER': '09',
            'OCTOBER': '10',
            'NOVEMBER': '11',
            'DECEMBER': '12',
        }

        if month.upper() not in month_map:
            sys.exit("SOMETHING WENT WRONG WITH MONTH MANIPULATION")
        else:
            month = month_map[month.upper()]
        date = f'{year}-{month}-{day}'

        # Calculate end time in military hours
        if (args.duration/60).is_integer() == True:
            discord_end_time = int(args.time + (args.duration/60 * 100))
        elif int(args.time + (args.duration//60 * 100 + 30)) % 100 == 60:
            discord_end_time = int(args.time + (args.duration//60 * 100 + 30)) - 60 + 100
        else:
            discord_end_time = int(args.time + (args.duration//60 * 100 + 30))

    # Books the room
    def book_room(self, unix_timestamp: str):
        global name

        browser.open_page('https://carletonu.libcal.com/r/accessible/availability?lid=2986&zone=0&gid=0&capacity=2&space=')

        self.click_button(by=By.ID, value='date')  # Select dropdown menu
        select = Select(self.browser.find_element(by=By.ID,value='date'))
        select.select_by_value(date)
        self.click_button(by=By.ID, value='s-lc-submit-filters')  # Select dropdown menu
        time.sleep(2)

        # Calculate seconds of time to add to 12:00AM
        if (args.time/100).is_integer() == True:
            start = int(args.time/100 * 60) * 60
        else:
            start = int(args.time//100 * 60 + 30) * 60
        current_timestamp = int(unix_timestamp) + start
        end_timestamp = current_timestamp + args.duration * 60

        # Click the times to book them
        while(current_timestamp != end_timestamp):
            self.click_button(by=By.ID, value=f's{room_id}_0_{current_timestamp}')
            current_timestamp += 1800

        self.click_button(by=By.ID, value='s-lc-submit-times')  # Submit Times
        self.click_button(by=By.ID, value='terms_accept')  # Continue

        name = self.browser.find_element(by=By.CLASS_NAME, value='s-lc-session-aware-link').text.split()[:2]  # Click on the first 'Book' button

        self.click_button(by=By.ID, value='btn-form-submit')  # Submit my Booking
        if self.browser.find_elements(by=By.CLASS_NAME, value='jquery-notification-error'):
            raise Exception()
        time.sleep(1)


# Main Function
if __name__ == '__main__':
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='An automated booking script for Carleton Library rooms')
    PRINTING_PADDING = 45

    # Initialize argparse
    initialize_parser(parser)

    # Parse the args
    args = parser.parse_args()
    parse_args(args)

    # Instantiate the discord webhook
    discord = Discord(url=DISCORD_WEBHOOK)
    
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
    print(f"\n{'ENSURING LATEST VERSION OF CHROMEDRIVER':-^{PRINTING_PADDING}}\n")
    driver_manager.main()
    time.sleep(2)

    # Support for different architectures
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
    
    print(f"\n{'GETTING UNIX TIMESTAMP AND DATE':-^{PRINTING_PADDING}}\n")
    try:
        unix_timestamp = browser.get_unix_timestamp()
        browser.get_date()
        print(f"{'SUCCESS':-^{PRINTING_PADDING}}\n\n\n")
    except:
        print(f"{'FAILED TO GET TIMESTAMP':-^{PRINTING_PADDING}}\n")
        print(f"{'EXITING PROGRAM':-^{PRINTING_PADDING}}\n\n")
        exit()
    print(f"{'LOGGING IN TO CARLETON CENTRAL':-^{PRINTING_PADDING}}\n")
    try:
        browser.login_carleton(username, password)
        print(f"{'SUCCESS':-^{PRINTING_PADDING}}\n\n\n")
    except:
        print(f"{'FAILED TO LOGIN':-^{PRINTING_PADDING}}\n")
        print(f"{'PLEASE CHECK CREDENTIALS':-^{PRINTING_PADDING}}\n")
        print(f"{'EXITING PROGRAM':-^{PRINTING_PADDING}}\n\n")
        exit()
    print(f"{'ATTEMPTING TO BOOK ROOM':-^{PRINTING_PADDING}}\n")
    try:
        browser.book_room(unix_timestamp)
        print(f"{'SUCCESS':-^{PRINTING_PADDING}}\n\n\n")
    except:
        print(f"{'FAILED TO BOOK ROOM':-^{PRINTING_PADDING}}\n")
        print(f"{'ROOM MIGHT BE UNAVAILABLE TO BOOK':-^{PRINTING_PADDING}}")
        print(f"{'OR DESIRED TIMESLOT UNAVAILABLE':-^{PRINTING_PADDING}}")
        print(f"{'OR EXCEEDED DAILY 6 HOUR LIMIT':-^{PRINTING_PADDING}}\n")
        print(f"{'EXITING PROGRAM':-^{PRINTING_PADDING}}\n\n")
        exit()
    try:
        print(f"{'POSTING TO DISCORD':-^{PRINTING_PADDING}}\n")
        time.sleep(random.randint(0,10))  # Sleep to circumvent discord rate limit
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
        print(f"{'SUCCESS':-^{PRINTING_PADDING}}\n\n\n")
    except:
        print(f"{'FAILED TO POST TO DISCORD':-^{PRINTING_PADDING}}\n\n")

    browser.close_browser
