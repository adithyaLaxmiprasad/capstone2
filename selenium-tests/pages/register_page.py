from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegisterPage:

    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = f"{base_url}register"

    def open(self):
        self.driver.get(self.url)

    def register(self, first_name, last_name, email, password):
        self.driver.find_element(By.ID, "FirstName").send_keys(first_name)
        self.driver.find_element(By.ID, "LastName").send_keys(last_name)
        self.driver.find_element(By.ID, "Email").send_keys(email)
        self.driver.find_element(By.ID, "Password").send_keys(password)
        self.driver.find_element(By.ID, "ConfirmPassword").send_keys(password)

        self.driver.find_element(By.ID, "register-button").click()

        msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "result"))
        ).text

        return msg
