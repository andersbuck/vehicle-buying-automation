from selenium import webdriver
import os
import sys
import time
import copartscrape

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

copartscrape.scrape(driver)

driver.close()