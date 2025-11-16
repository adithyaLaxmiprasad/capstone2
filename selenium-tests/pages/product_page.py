from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductPage:
    TITLE = (By.CSS_SELECTOR, "div.product-name h1")
    ADD_TO_CART = (By.ID, "add-to-cart-button-4")

    def __init__(self, driver):
        self.driver = driver

    def get_title(self):
        return WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.TITLE)
        ).text

    def add_to_cart(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ADD_TO_CART)
        ).click()
