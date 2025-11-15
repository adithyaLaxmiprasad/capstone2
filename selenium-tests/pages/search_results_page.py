from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchResultsPage:
    FIRST_PRODUCT = (By.CSS_SELECTOR, "h2.product-title a")

    def __init__(self, driver):
        self.driver = driver

    def first_product_title(self):
        el = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.FIRST_PRODUCT)
        )
        return el.text.strip()

    def open_first_product(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.FIRST_PRODUCT)
        ).click()
