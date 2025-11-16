from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductPage:

    TITLE = (By.CSS_SELECTOR, "div.product-name h1")
    ADD_BTN = (By.ID, "add-to-cart-button-4")

    def __init__(self, driver):
        self.driver = driver

    def get_title(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.TITLE)
        ).text
