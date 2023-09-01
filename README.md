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
- discordwebhook
- Git


<br></br>
## How to Run <a name="run"></a>
- Clone this GitHub repo
- Pre-requisites
  - python3
  - selenium
    - `pip install selenium`
  - discordwebhook
    - `pip install discordwebhook`
    - This project contains a hardcoded Discord Webhook to a private server. To use your own webhook, just modify the `DISCORD_WEBHOOK` definition to your own url
  - Google Chrome version 115+
    - To check Chrome version: chrome://settings/help
    - The Windows, Linux, and MacOS ChromeDrivers for Chrome version `115.0.5790.170` can be found in drivers/ but if you are using a Chrome version older than that, you must download the compatible ChromeDriver for your version from https://chromedriver.chromium.org/downloads
      - Apparently you may be able to use the provided ChromeDriver version with older versions of Chrome, but if you can't, follow the previous step
  - It's recommended that you run both Google Chrome and the ChromeDriver executable for your arch at least once before using this script
  - Update the `name` and `email` for your booking in credentials.py keeping it as a string
    - If you don't wish to hardcode your credentials, you can pass them in as command line arguments with `-n NAME -e EMAIL`
- To run Autobook.py
  - `python3 Autobook.py -d [DATE] -r [ROOM_NUMBER] -t [TIME]`
  - You can run `python3 Autobook.py -h` to print the usages for a more detailed explanation of the flags
  - You can optionally use the `--duration` flag to specify a booking duration
  - You can optionally use the `--headless` flag to run the program headlessly
  - An example command if you were trying to book room 570 at 10:00 AM for next Monday:
      - `python3 Autobook.py -d monday -r 570 -t 1000 --headless`
