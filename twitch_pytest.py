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

# This import is used for the `@pytest.fixture` decorator.
# The `@pytest.fixture` decorator is used to define a fixture, which is a function that provides a resource or setup for tests.
# In this case, the `browser` fixture sets up a Selenium WebDriver instance with specific options (such as window size and mobile emulation) and yields it to the test function.

@pytest.fixture
def browser():
    #
    # This fixture sets up a Selenium WebDriver instance with specific options (such as window size and mobile emulation) and yields it to the test function.
    #
    options = Options()
    options.add_argument("--window-size=500,800")

    # This sets the mobile emulation options for the browser.
    # In this case, it sets the device name to "iPhone X".
    mobile_emulation = {"deviceName": "iPhone X"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    # This creates a service object for the ChromeDriver.
    # The service object is used to manage the ChromeDriver process.
    service = Service("/home/mrproject/source_code/chromedriver")

    # This creates a new WebDriver instance using the ChromeDriver service and the specified options.
    browser = webdriver.Chrome(service=service, options=options)

    # The `yield` statement yields the browser instance to the test function.
    # After the test function has finished executing, the `browser.quit()` method will be called to close the browser instance and release any resources it was using.
    yield browser

    browser.quit()


def test_second_event_live(browser):
    #
    # This test function searches for "StarCraft II" on Twitch, clicks on the second search result, and saves a screenshot of the streamer's video.
    #
    browser.get("https://www.twitch.tv/")
    
    try:
        # This tries to locate and click the privacy popup.
        # If the privacy popup is not present or cannot be clicked within 2 seconds, the `except` block is executed and the script continues without clicking the popup.
        privacy_popup = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="ScCoreButtonLabel-sc"]'))
        )
        privacy_popup.click()
    except TimeoutException:
        pass

    # This tries to locate and click the search box.
    # If the search box is not present or cannot be clicked within 2 seconds, the `except` block is executed and the script continues without clicking the search box.
    search_box = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Search"]'))
        )
    search_box.click()

    # This locates the search input field and enters "StarCraft II" into the field.
    search_input = browser.find_element(By.CSS_SELECTOR, "input[type='search']")
    search_input.send_keys('StarCraft II')

    # This sends the Enter key to the search input field, which triggers the search.
    search_input.send_keys(Keys.ENTER)
    time.sleep(3)

    # This locates the search results and clicks on the second search result.
    search_results = browser.find_elements(By.CSS_SELECTOR, "a[class^='ScCoreLink-sc']")
    search_results[2].click()

    # This creates a WebDriverWait object and waits for a video element to be present on the page, indicating that the search results have loaded.
    wait = WebDriverWait(browser, 5)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))

    # This saves a screenshot of the current browser window to a file named "streamer_screenshot.png".
    browser.save_screenshot("streamer_screenshot.png")
