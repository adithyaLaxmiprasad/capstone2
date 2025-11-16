from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    SEARCH_INPUT = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.search-box-button")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = base_url

    def open(self):
        self.driver.get(self.url)

    def search(self, text):
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        ).send_keys(text)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        ).click()
