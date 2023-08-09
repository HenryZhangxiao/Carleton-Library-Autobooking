## Introduction

A headless program designed to automate the process of booking Carleton Library rooms.

The inspiration for this project comes from the tiresome process of needing to book a room nearly every day. This program simply automates the entire process.


#### Table of Contents
- [Technologies Used ](#technologies)
- [How to Run ](#run)


<br></br>
## Technologies Used <a name="technologies"></a>
- Python3
- Selenium
- WebDriver
- ChromeDriver
- Git


<br></br>
## How to Run <a name="run"></a>
- Clone this GitHub repo
- Pre-requisites
  - python3
  - selenium
    - `pip install selenium`
  - Google Chrome version 115+
    - To check Chrome version: chrome://settings/help
    - The Windows, Linux, and MacOS ChromeDrivers for Chrome version `115.0.5790.170` can be found in drivers/ but if you are using a Chrome version older than that, you must download the compatible ChromeDriver for your version from https://chromedriver.chromium.org/downloads
      - Apparently you may be able to use the provided ChromeDriver version with older versions of Chrome, but if you can't, follow the previous step
  - It's recommended that you run both Google Chrome and the ChromeDriver executable for your arch at least once before using this script
  - Update the `username` and `password` for your MC1 login in credentials.py keeping it as a string
    - If you don't wish to hardcode your credentials, you can pass them in as command line arguments with `-u USERNAME -p PASSWORD`
- To run Autobook.py
  - `python3 Autobook.py -r [ROOM_NUMBER] -d [DATE] -t [TIME]`
  - You can run `python3 Autobook.py -h` to print the usages for a more detailed explanation of the flags
  - You can optionally use the `--duration` flag to specify a booking duration
  - You can optionally use the `--headless` flag to run the program headlessly
  - An example command if you were trying to book room 570 at 10:00 AM for next Monday:
      - `python3 Autobook.py -d monday -r 570 -t 1000 --headless`
