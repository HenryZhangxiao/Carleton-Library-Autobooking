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
  - You must make sure you have run both Google Chrome and the ChromeDriver executable for your arch at least once
  - Update the `username` and `password` in credentials.py keeping it as a string
- To run Autobook.py
  - `python3 Autobook.py -r [ROOM_NUMBER] -d [DATE] -t [TIME]`
  - You can run `python3 Autobook.py -h` to print the usages for a more detailed explanation of the flags
  - You can optionally use the `--duration` flag to specify a booking duration