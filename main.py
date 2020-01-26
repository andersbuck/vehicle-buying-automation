from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

# Now you can start using Selenium

#driver.get("https://mobile.facebook.com/marketplace/charlotte/?radius_in_km=161&query=jeep+cherokee")
driver.get("https://www.facebook.com/marketplace/charlotte/vehicles/?vehicleMake=Jeep&vehicleModel=Jeep%20Cherokee&minVehicleYear=1997&maxVehicleYear=2001&sort=CREATION_TIME_DESCEND")
print(driver.page_source)