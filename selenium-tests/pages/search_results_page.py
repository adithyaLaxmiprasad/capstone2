from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchResultsPage:

    PRODUCT_TITLES = (By.CSS_SELECTOR, "h2.product-title a")

    def __init__(self, driver):
        self.driver = driver

    def first_product_title(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.PRODUCT_TITLES)
        ).text

    def open_first_product(self):
        self.driver.find_elements(*self.PRODUCT_TITLES)[0].click()
