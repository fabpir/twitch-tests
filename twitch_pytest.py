import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import subprocess

@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--window-size=500,800")

    mobile_emulation = {"deviceName": "iPhone X"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    service = Service("/home/mrproject/source_code/chromedriver")
    browser = webdriver.Chrome(service=service, options=options)

    yield browser

    browser.quit()


def test_second_event_live(browser):
    browser.get("https://www.twitch.tv/")
    
    try:
        privacy_popup = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="ScCoreButtonLabel-sc"]'))
        )
        privacy_popup.click()
    except TimeoutException:
        pass
    time.sleep(2)
    #search_box = browser.find_element (By.CSS_SELECTOR, 'a[href="/search"]')
    try:
        search_box = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Search"]'))
        )
        search_box.click()
    except TimeoutException:
        pass

    search_input = browser.find_element(By.CSS_SELECTOR, "input[type='search']")
    search_input.send_keys('StarCraft II')
    # either press the enter key
    search_input.send_keys(Keys.ENTER)
    time.sleep(2)
    
    search_results = browser.find_elements(By.CSS_SELECTOR, "a[class^='ScCoreLink-sc']")
    search_results[2].click()
    # Add a delay to allow search results to load
    time.sleep(2)  # Adjust the delay as needed

    #if len(search_results) >= 2:
    #    second_result = search_results[1]
    #    second_result.click()
    #    print ("Total Results", len(search_results))
    #else:
    #    print("Insufficient search results:", len(search_results))
   
    wait = WebDriverWait(browser, 5)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))

    browser.save_screenshot("streamer_screenshot.png")
    browser.quit()