# selenium-tests/pages/order_confirmation_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrderConfirmationPage:
    THANK_YOU_SECTION = (By.CSS_SELECTOR, "div.section.order-completed")

    def __init__(self, driver, wait_time: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_time)

    def wait_for_thankyou_page(self) -> bool:
        """
        Wait for the order-completed section to be visible.
        Returns True if visible within timeout, else False.
        """
        try:
            el = self.wait.until(EC.visibility_of_element_located(self.THANK_YOU_SECTION))
            text = el.text.lower()
            return "thank you" in text or "order" in text
        except Exception:
            return False
