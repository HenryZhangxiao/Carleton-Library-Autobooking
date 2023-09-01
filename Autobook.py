# Import the required modules
# from selenium import webdriver #deprecated
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from discordwebhook import Discord
import credentials
import room_id as room_ids
import math
import time
import argparse
import platform
import os
import sys
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

parser.add_argument('-n', '--name', type=str, required=False,
                    help='Full name for booking. This will take precedence over credentials.py name')

parser.add_argument('-e', '--email', type=str, required=False,
                    help='Email for booking. This will take precedence over credentials.py email')

parser.add_argument('--duration', type=int, default=180, required=False,
                    help='Desired duration of your booking in minutes. 30 minute increments; Max 180 minutes. Default 180 minutes')

parser.add_argument('--headless', action='store_true', default=False, required=False,
                    help='Runs the program in headless mode (Does not open the browser). Default is false')

args = parser.parse_args()
args.date = ' '.join(args.date)
args.room=args.room.upper()
if args.name is not None and args.email is not None:
    name, email = args.name, args.email
else:
    name, email = credentials.name, credentials.email
room_id = room_ids.room_ids[args.room]
date = day = month = year = discord_day = discord_month = ''
discord_end_time=0
DISCORD_WEBHOOK = 'https://discord.com/api/webhooks/1147262918199611484/mQyvGE3rE1MKGXpFLjKYKicyjyeV_Q7tvq3BVp9TdenHOQSk2qMohPGnHV5tiAoIA90l'
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
        time.sleep(0.5)
        
    #Clicks button found by [by] with identifier [value]
    def click_button(self, by: By, value: str): 
        button = self.browser.find_element(by=by, value=value)
        button.click()
        time.sleep(1)
        
    #Gets the unix timestamp for the date and returns it
    def get_unix_timestamp(self) -> str:
        global date, day, month, year, discord_day
        match args.date.upper():
            case "SUNDAY" | "SUN":
                browser.open_page('https://www.unixtimesta.mp/saturday')
                timestamp = str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
                browser.open_page('https://www.unixtimesta.mp/'+timestamp)
                date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
                day=date[0]
                month=date[1]
                year=date[2]
                discord_day='Sunday'
                return timestamp
            case "MONDAY" | "MON":
                browser.open_page('https://www.unixtimesta.mp/sunday')
                timestamp = str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
                browser.open_page('https://www.unixtimesta.mp/'+timestamp)
                date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
                day=date[0]
                month=date[1]
                year=date[2]
                discord_day='Monday'
                return timestamp
            case "TUESDAY" | "TUE" | "TUES":
                browser.open_page('https://www.unixtimesta.mp/monday')
                timestamp = str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
                browser.open_page('https://www.unixtimesta.mp/'+timestamp)
                date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
                day=date[0]
                month=date[1]
                year=date[2]
                discord_day='Tuesday'
                return timestamp
            case "WEDNESDAY" | "WED":
                browser.open_page('https://www.unixtimesta.mp/tuesday')
                timestamp = str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
                browser.open_page('https://www.unixtimesta.mp/'+timestamp)
                date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
                day=date[0]
                month=date[1]
                year=date[2]
                discord_day='Wednesday'
                return timestamp
            case "THURSDAY" | "THU" | "THURS":
                browser.open_page('https://www.unixtimesta.mp/wednesday')
                timestamp = str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
                browser.open_page('https://www.unixtimesta.mp/'+timestamp)
                date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
                day=date[0]
                month=date[1]
                year=date[2]
                discord_day='Thursday'
                return timestamp
            case "FRIDAY" | "FRI":
                browser.open_page('https://www.unixtimesta.mp/thursday')
                timestamp = str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
                browser.open_page('https://www.unixtimesta.mp/'+timestamp)
                date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
                day=date[0]
                month=date[1]
                year=date[2]
                discord_day='Friday'
                return timestamp
            case "SATURDAY" | "SAT":
                browser.open_page('https://www.unixtimesta.mp/friday')
                timestamp = str(int(self.browser.current_url.replace("https://www.unixtimesta.mp/", "")) + 86400)
                browser.open_page('https://www.unixtimesta.mp/'+timestamp)
                date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
                day=date[0]
                month=date[1]
                year=date[2]
                discord_day='Saturday'
                return timestamp
            case _:
                browser.open_page('https://www.unixtimesta.mp/' + args.date.replace(" ", ""))
                date = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[1].split(" ")
                discord_day = self.browser.find_element(by=By.ID, value="utctime").text.split(", ")[0].split(" ")[-1]
                day=date[0]
                month=date[1]
                year=date[2]
                return self.browser.current_url.replace("https://www.unixtimesta.mp/", "")
            
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
        else:
            discord_end_time = int(args.time + (math.floor(args.duration/60) * 100 + 30))
    #Books the room
    def book_room(self, unix_timestamp: str):
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

        self.add_input(by=By.ID, value='fname', text=credentials.name.split(" ")[0])
        self.add_input(by=By.ID, value='lname', text=credentials.name.split(" ")[1])
        self.add_input(by=By.ID, value='email', text=credentials.email)
        self.click_button(by=By.ID, value='btn-form-submit') #Submit my Booking
        if self.browser.find_elements(by=By.CLASS_NAME, value='jquery-notification-error'):
            raise Exception()
        time.sleep(1)


# Main Function
if __name__ == '__main__':
    #Support for different architectures
    if platform.system() == "Windows":
        os.chmod('drivers\chromedriver.exe', stat.S_IRWXU)
        browser = Browser('drivers\chromedriver.exe')
    elif platform.system() == "Darwin":
        os.chmod('drivers/chromedriver_mac', stat.S_IRWXU)
        browser = Browser('drivers/chromedriver_mac')
    elif platform.system() == "Linux":
        os.chmod('drivers/chromedriver_linux', stat.S_IRWXU)
        browser = Browser('drivers/chromedriver_linux')
    discord = Discord(url=DISCORD_WEBHOOK)

    print("\n-------GETTING UNIX TIMESTAMP AND DATE-------\n")
    try:
        unix_timestamp = str(int(browser.get_unix_timestamp()) + 14400)
        browser.get_date()
        print("-------------------SUCCESS-------------------\n\n\n")
    except:
        print("-----------FAILED TO GET TIMESTAMP-----------\n")
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
        start_time = str(args.time).zfill(4)
        end_time = str(discord_end_time).zfill(4)
        discord.post(
            username=f'{credentials.name.split(" ")[0]} {credentials.name.split(" ")[1]}',
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
