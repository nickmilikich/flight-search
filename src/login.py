import keyboard
import time

from config import CONFIG, CREDENTIALS
from selenium.webdriver.common.by import By

def login(driver):

    # Open login screen
    driver.get("https://www.pointsyeah.com/login")

    # Click on username
    driver.find_element(By.CSS_SELECTOR, "div.amplify-field:nth-child(2) > div:nth-child(2) > div:nth-child(1)").click()
    # Type username
    time.sleep(2)
    keyboard.write(CREDENTIALS["username"])

    # Click on password
    driver.find_element(By.CSS_SELECTOR, "div.amplify-flex:nth-child(3) > div:nth-child(2) > div:nth-child(1)").click()
    # Type password
    time.sleep(2)
    keyboard.write(CREDENTIALS["password"])

    # Submit credentials
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button.amplify-button:nth-child(2)").click()

    # Navigate to main page
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, ".w-\[260px\]").click()