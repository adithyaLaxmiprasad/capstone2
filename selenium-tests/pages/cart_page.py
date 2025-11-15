from selenium.webdriver.common.by import By

class CartPage:
    TERMS_CHECKBOX = (By.ID, "termsofservice")
    CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("https://demo.nopcommerce.com/cart")

    def proceed_to_checkout(self):
        self.driver.find_element(*self.TERMS_CHECKBOX).click()
        self.driver.find_element(*self.CHECKOUT_BTN).click()
