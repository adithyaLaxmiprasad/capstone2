from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    SEARCH_INPUT = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CART_ICON = (By.CSS_SELECTOR, "span.cart-qty")

    def __init__(self, driver, base_url):
        self.driver = driver
        # ensure base_url ends with trailing slash
        self.base_url = base_url if base_url.endswith("/") else base_url + "/"

    def open(self):
        self.driver.get(self.base_url)

    def search(self, keyword):
        # clear, type and submit; wait for results to appear
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SEARCH_INPUT)).clear()
        self.driver.find_element(*self.SEARCH_INPUT).send_keys(keyword)
        self.driver.find_element(*self.SEARCH_BUTTON).click()

    def cart_quantity(self):
        # cart-qty text is like "(1)"; handle gracefully
        try:
            text = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.CART_ICON)
            ).text.strip()
            # strip parentheses and whitespace
            text = text.strip("() ").strip()
            return int(text) if text.isdigit() else 0
        except Exception:
            return 0
