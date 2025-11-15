# selenium-tests/utils/driver_factory.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

def create_driver(headless: bool = True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # enable browser console logging
    caps = DesiredCapabilities.CHROME.copy()
    caps["goog:loggingPrefs"] = {"browser": "ALL", "performance": "ALL"}

    # webdriver-manager downloads a driver matching the installed Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options, desired_capabilities=caps)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(5)
    return driver
