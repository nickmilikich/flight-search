import datetime
import keyboard
import pandas as pd
import time

from config import CONFIG, CREDENTIALS
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def run_searches(driver):

    # Get all dates between start and end
    start_dates = pd.date_range(
        start=CONFIG["dates"]["start_date"],
        end=CONFIG["dates"]["end_date"],
        # Filter to relevant days of the week
    )
    start_dates = [
        start_date for start_date in start_dates
        if start_date.strftime("%A") in CONFIG["dates"]["window_start"]
    ]
    print(f"start_dates {start_dates}")

    # Loop through searches
    for destination in CONFIG["destinations"].keys():

        # Loop through departure airports
        for departure, max_stops in CONFIG["destinations"][destination].items():

            # Loop through start dates
            for start_date in start_dates:

                # Perform one search
                print(f"Performing search for {departure} -> {destination} {start_date.strftime('%Y-%m-%d')}")
                perform_one_search(
                    driver=driver,
                    destination=destination,
                    departure=departure,
                    max_stops=max_stops,
                    window_start=start_date,
                    new_destination=(destination != old_distination if "old_distination" in locals() else "start"),
                    new_departure=(departure != old_departure if "old_departure" in locals() else "start"),
                )
                old_distination = destination
                old_departure = departure

def perform_one_search(
    driver,
    destination,
    departure,
    max_stops,
    window_start,
    new_destination,
    new_departure,
):

    # Open a new window
    driver.execute_script("window.open('');")
    
    # Switch to the new window and open search URL
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("https://www.pointsyeah.com")

    # Select fare class
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.select-block:nth-child(3)"))).click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#rc_select_2_list_1 > div:nth-child(1)"))).click()

    if new_departure or (new_departure == "start"):
        # Click on departing from
        time.sleep(1)
        # Try selecting selection item; except select selection search
        try:
            driver.find_element(By.CSS_SELECTOR, "div.action-item:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").click()
        except:
            driver.find_element(By.CSS_SELECTOR, "div.action-item:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)").click()
        # Type departure
        time.sleep(2)
        keyboard.write(departure)
        time.sleep(1)
        keyboard.send("down")
        keyboard.write("\n")

    # If changing destinations, type the new one
    if new_destination or (new_destination == "start"):
        # Click on going to
        time.sleep(1)
        # Try selecting selection item; except select selection search
        try:
            driver.find_element(By.CSS_SELECTOR, "div.action-item:nth-child(3) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").click()
        except:
            driver.find_element(By.CSS_SELECTOR, "div.action-item:nth-child(3) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)").click()
        # Type destination
        time.sleep(2)
        keyboard.write(destination)
        time.sleep(1)
        # if new_destination != "start":
        keyboard.send("down")
        keyboard.write("\n")

    # Click on departure date start
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ant-picker-input:nth-child(1) > input:nth-child(1)"))).click()
    # Type destination
    time.sleep(2)
    keyboard.write(window_start.strftime("%Y-%m-%d"))

    # Click on departure date end
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ant-picker-input:nth-child(3) > input:nth-child(1)"))).click()
    # Type destination
    time.sleep(2)
    keyboard.write((window_start + datetime.timedelta(days=3)).strftime("%Y-%m-%d") + "\n")

    # Click search
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".text-\[16px\]console\.assert\(expression\,"))).click()
    
    # Close old search tab
    driver.close()
    # Switch to new tab opened
    driver.switch_to.window(driver.window_handles[-1])

    # Filter premium cabin percentage
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ant-space-item:nth-child(8)"))).click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-radio-group > div:nth-child(4) > label:nth-child(1) > span:nth-child(2)"))).click()

    # Filter by number of stops
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-col-xs-24 > div:nth-child(1) > div:nth-child(3)"))).click()
    if max_stops == 0:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.h-\[36px\]:nth-child(2) > label:nth-child(1)"))).click()
    elif max_stops == 1:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.h-\[36px\]:nth-child(3) > label:nth-child(1)"))).click()
    elif max_stops == 2:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.h-\[36px\]:nth-child(4) > label:nth-child(1)"))).click()

    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(9) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(2)"))).click()
    except:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(8) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(2)"))).click()