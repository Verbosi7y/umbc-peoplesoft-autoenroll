from selenium import webdriver
from selenium.webdriver.common.by import By

import time
from datetime import datetime

import json
# import random

def get_url():
    with open('config.json') as f:
        config = json.load(f)
        return config['url']
    

def get_login():
    with open('config.json') as f:
        config = json.load(f)
        return config['login']


def check_login(driver):
    try:
        driver.find_element(By.ID, 'login')
        return True

    except:
        return False
    

def check_duo(driver):
    duo_str = "duosecurity.com"

    if duo_str in driver.current_url:
        return True
    
    return False


def login(driver, username, password):
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'submitButton').click()

    time.sleep(5)

    if not check_login(driver):
        print("INFO: UMBC Login successful => Possibly verifying with Duo Push next")
    else:
        print("ERROR: Login failed")
        driver.close()
        exit(1)

    attempts = 1
    max_attempt = 2
    while check_duo(driver) and attempts <= max_attempt:
        time.sleep(5)

        try: # On success, the first trust browser button will be found 
            driver.find_element(By.ID, 'trust-browser-button').click() # Click on the first trust browser button

            time.sleep(5) # Wait for the trust browser to load
        except:
            print("INFO: No trust browser button found yet")

        # Duo Push timed out after 60 seconds
        try: # Note: If Duo Push times out around 5 times, the account would be locked out
            driver.find_element(By.CLASS_NAME, 'try-again-button').click()
            print(f"WARNING: Duo Push timed out. Trying again... Attempt: {attempts}/{max_attempt}")

            attempts += 1
        except:
            print("INFO (Ignore): No try again button found")

        if "csprd-web.ps.umbc.edu" in driver.current_url:
            print("INFO: Duo Push successful")
            break

    if attempts > max_attempt:
        print("ERROR: Failed to login. Exiting...")
        driver.close()
        exit(1)


def main():
    cred = get_login()

    driver = webdriver.Chrome()
    
    driver.implicitly_wait(5)
    driver.get(get_url())

    require_login = check_login(driver)

    if require_login:
        login(driver, cred['username'], cred['password'])

    open_bool = False
    while True:
        seats_open = driver.find_elements(By.CLASS_NAME, 'sr-only')[7].text

        print(str(datetime.now()) + ': ' + 'Status: ' + seats_open)

        if not open_bool and '0 of' not in seats_open:
            print(str(datetime.now()) + ': ' + 'Seats are now opened: ' + seats_open)
            open_bool = True

            # Click on the Enroll button
            enroll_button = driver.find_elements(By.XPATH, "//button[@class='cx-MuiButtonBase-root cx-MuiButton-root cx-MuiButton-contained cx-MuiButton-containedPrimary']")[1]
            enroll_button.click()

            # Click on Save button to fully enroll
            save_button = driver.find_element(By.XPATH, "//button[@class='cx-MuiButtonBase-root cx-MuiButton-root cx-MuiButton-contained cx-MuiButton-containedPrimary cx-MuiButton-fullWidth']")
            save_button.click()

            print(str(datetime.now()) + ': ' + 'Enrolled successfully!')

            break # Exit the while loop

        if open_bool and '0 of' in seats_open:
            print(str(datetime.now()) + ': ' + 'Seats are closed!')
            open_bool = False

        driver.refresh()
        time.sleep(300) # Refresh every 5 minutes

        # Check if session is about to expire and click
        try:
            driver.find_element(By.ID, 'msgokbutton').click()
            print("INFO: Session about to expire, clicking ok button")

            time.sleep(5)
        except:
            pass

    driver.close() # Close the browser

main()
