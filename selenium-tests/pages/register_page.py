from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegisterPage:

    FIRSTNAME = (By.ID, "FirstName")
    LASTNAME = (By.ID, "LastName")
    EMAIL = (By.ID, "Email")
    PASSWORD = (By.ID, "Password")
    CONFIRM_PASSWORD = (By.ID, "ConfirmPassword")
    REGISTER_BTN = (By.ID, "register-button")
    SUCCESS_MSG = (By.CLASS_NAME, "result")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = f"{base_url}register"

    def open(self):
        self.driver.get(self.url)

        # 🔥 IMPORTANT: wait for form to load
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.FIRSTNAME)
        )

    def register(self, first_name, last_name, email, password):

        self.driver.find_element(*self.FIRSTNAME).send_keys(first_name)
        self.driver.find_element(*self.LASTNAME).send_keys(last_name)
        self.driver.find_element(*self.EMAIL).send_keys(email)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.CONFIRM_PASSWORD).send_keys(password)

        self.driver.find_element(*self.REGISTER_BTN).click()

        message = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.SUCCESS_MSG)
        ).text

        return message
