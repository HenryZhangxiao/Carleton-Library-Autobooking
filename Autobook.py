# Import the required modules
# from selenium import webdriver #deprecated
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import credentials
import time
import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')

class Browser:
    browser, service = None, None
    
    def __init__(self, driver: str):
        self.service = Service(driver)
        self.browser = webdriver.Chrome(service=self.service)

    def open_page(self, url: str):
        self.browser.get(url)

    def close_browser(self):
        self.browser.close()

    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(1)

    def click_button(self, by: By, value: str):
        button = self.browser.find_element(by=by, value=value)
        button.click()
        time.sleep(1)

    def login_booking_carleton(self, username: str, password: str):
        self.click_button(by=By.ID, value='spanLogin')
        self.add_input(by=By.ID, value='txtUsername', text=username)
        self.add_input(by=By.ID, value='txtPassword', text=password)
        time.sleep(2)
        self.click_button(by=By.ID, value='btnLogin')

    def book_room(self, room: str):
        self.add_input(by=By.ID, value='listSearch', text=room)
        time.sleep(1)
        self.click_button(by=By.CLASS_NAME, value='SearchHighlight')
        time.sleep(1)
        self.click_button(by=By.ID, value='cboDuration')
        select = Select(self.browser.find_element(by=By.ID,value='cboDuration'))
        select.select_by_visible_text('03:00')


# Main Function
if __name__ == '__main__':

    browser = Browser('drivers\chromedriver.exe')
    browser.open_page('https://booking.carleton.ca/')
    time.sleep(3)
    browser.login_booking_carleton(credentials.username, credentials.password)
    time.sleep(3)
    browser.open_page('https://booking.carleton.ca/index.php?p=BookRoom&r=1')
    time.sleep(5)
    browser.book_room('570')
    time.sleep(8)
    browser.close_browser
"""


    # Provide the email and password
    email = 'example@example.com'
    password = 'password'

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')

    # Provide the path of chromedriver present on your system.
    driver = webdriver.Chrome(executable_path="C:/chromedriver/chromedriver.exe",
                            chrome_options=options)
    driver.set_window_size(1920,1080)

    # Send a get request to the url
    driver.get('https://auth.geeksforgeeks.org/')
    time.sleep(5)

    # Finds the input box by name in DOM tree to send both
    # the provided email and password in it.
    driver.find_element_by_name('user').send_keys(email)
    driver.find_element_by_name('pass').send_keys(password)
    
    # Find the signin button and click on it.
    driver.find_element_by_css_selector(
        'button.btn.btn-green.signin-button').click()
    time.sleep(5)

    # Returns the list of elements
    # having the following css selector.
    container = driver.find_elements_by_css_selector(
        'div.mdl-cell.mdl-cell--9-col.mdl-cell--12-col-phone.textBold')
    
    # Extracts the text from name,
    # institution, email_id css selector.
    name = container[0].text
    try:
        institution = container[1].find_element_by_css_selector('a').text
    except:
        institution = container[1].text
    email_id = container[2].text

    # Output Example 1
    print("Basic Info")
    print({"Name": name,
        "Institution": institution,
        "Email ID": email})

    # Clicks on Practice Tab
    driver.find_elements_by_css_selector(
    'a.mdl-navigation__link')[1].click()
    time.sleep(5)

    # Selected the Container containing information
    container = driver.find_element_by_css_selector(
    'div.mdl-cell.mdl-cell--7-col.mdl-cell--12-col-phone.\
    whiteBgColor.mdl-shadow--2dp.userMainDiv')
    
    # Selected the tags from the container
    grids = container.find_elements_by_css_selector(
    'div.mdl-grid')
    
    # Iterate each tag and append the text extracted from it.
    res = set()
    for grid in grids:
        res.add(grid.text.replace('\n',':'))

    # Output Example 2
    print("Practice Info")
    print(res)

    # Quits the driver
    driver.close()
    driver.quit()
"""