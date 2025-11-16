from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchResultsPage:
    PRODUCT_TITLES = (By.CSS_SELECTOR, "h2.product-title a")

    def __init__(self, driver):
        self.driver = driver

    def first_product_title(self):
        return WebDriverWait(self.driver, 15).until(
            EC.visibility_of_all_elements_located(self.PRODUCT_TITLES)
        )[0].text

    def open_first_product(self):
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.PRODUCT_TITLES)
        )[0].click()
