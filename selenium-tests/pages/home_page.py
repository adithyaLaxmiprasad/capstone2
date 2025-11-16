from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    SEARCH_INPUT = (By.ID, "small-searchterms")
    SEARCH_BTN = (By.CSS_SELECTOR, "button.search-box-button")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = base_url

    def open(self):
        self.driver.get(self.url)

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )

    def search(self, text):
        box = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        box.clear()
        box.send_keys(text)

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.SEARCH_BTN)
        ).click()
