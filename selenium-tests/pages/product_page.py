from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductPage:
    # locator for title and add-to-cart button (id differs per product; generic attempt below)
    PRODUCT_TITLE = (By.CSS_SELECTOR, "div.product-name h1")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button.add-to-cart-button, input#add-to-cart-button-4")

    def __init__(self, driver):
        self.driver = driver

    def get_title(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.PRODUCT_TITLE)
        ).text.strip()

    def add_to_cart(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ADD_TO_CART_BTN)
        ).click()
