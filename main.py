from selenium import webdriver
import os
import sys
import time

# Configure Selenium 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

chrome_driver = None

isHerokuEnv = sys.argv[1]

if isHerokuEnv=='true':
    chrome_driver = os.environ.get("CHROMEDRIVER_PATH")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
else:
    chrome_driver = os.getcwd() + "/chromedriver_linux64/chromedriver"

driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)

# Start Selenium script

driver.get("https://www.facebook.com/marketplace/charlotte/vehicles/?vehicleMake=Jeep&vehicleModel=Jeep%20Cherokee&minVehicleYear=1997&maxVehicleYear=2001&sort=CREATION_TIME_DESCEND")
driver.implicitly_wait(10)

SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

content = driver.find_elements_by_css_selector('a._1oem')
for con in content:
    print(con.find_element_by_css_selector('div#marketplace-modal-dialog-title').get_attribute('title')
        + ' ' + con.find_element_by_css_selector('div._uc9').text
        + ' ' + con.find_element_by_css_selector('div._f3l').text)
    #print(con.get_attribute('alt'))