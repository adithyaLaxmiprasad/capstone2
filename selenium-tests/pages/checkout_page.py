# selenium-tests/pages/checkout_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    # Login (appears if user isn't logged in)
    LOGIN_EMAIL = (By.ID, "Email")
    LOGIN_PASSWORD = (By.ID, "Password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.login-button")

    # Cart -> Checkout
    TERMS_CHECKBOX = (By.ID, "termsofservice")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    # Checkout step continue buttons
    BILLING_CONTINUE = (By.CSS_SELECTOR, "button.new-address-next-step-button")
    SHIPPING_METHOD_CONTINUE = (By.CSS_SELECTOR, "button.shipping-method-next-step-button")
    PAYMENT_METHOD_CONTINUE = (By.CSS_SELECTOR, "button.payment-method-next-step-button")
    PAYMENT_INFO_CONTINUE = (By.CSS_SELECTOR, "button.payment-info-next-step-button")
    CONFIRM_ORDER_BUTTON = (By.CSS_SELECTOR, "button.confirm-order-next-step-button")

    def __init__(self, driver, base_url=None, wait_time: int = 20):
        self.driver = driver
        self.base_url = base_url.rstrip("/") + "/" if base_url else None
        self.wait = WebDriverWait(driver, wait_time)

    # Step 1 — From cart: click terms + checkout
    def begin_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.TERMS_CHECKBOX)).click()
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON)).click()

    # Step 2 — Login on checkout page (if login form is visible)
    # NOTE: this uses a test account; update credentials in conftest/env as needed.
    def login_checkout(self, email: str, password: str):
        # Wait for login fields (if they exist)
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_EMAIL)).clear()
        self.driver.find_element(*self.LOGIN_EMAIL).send_keys(email)
        self.driver.find_element(*self.LOGIN_PASSWORD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

        # After login you'll be redirected back to cart; re-click terms + checkout
        self.wait.until(EC.element_to_be_clickable(self.TERMS_CHECKBOX)).click()
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON)).click()

    # Step 3 — Complete the remaining checkout steps (click "Continue" repeatedly)
    def complete_checkout_steps(self):
        # The site might show intermediate wait screens, so we wait for buttons to be clickable
        self.wait.until(EC.element_to_be_clickable(self.BILLING_CONTINUE)).click()
        self.wait.until(EC.element_to_be_clickable(self.SHIPPING_METHOD_CONTINUE)).click()
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_CONTINUE)).click()
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_INFO_CONTINUE)).click()
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_ORDER_BUTTON)).click()
