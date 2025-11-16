from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class RegisterPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = f"{base_url}register"

    def open(self):
        self.driver.get(self.url)

        # Close cookie popup if appears
        try:
            btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, "eu-cookie-ok"))
            )
            self.driver.execute_script("arguments[0].click();", btn)
        except:
            pass

    def register(self, first, last, email, password):

        # Fill required fields
        self.driver.find_element(By.ID, "gender-male").click()

        Select(self.driver.find_element(By.NAME, "DateOfBirthDay")).select_by_value("1")
        Select(self.driver.find_element(By.NAME, "DateOfBirthMonth")).select_by_value("1")
        Select(self.driver.find_element(By.NAME, "DateOfBirthYear")).select_by_value("1990")

        self.driver.find_element(By.ID, "FirstName").send_keys(first)
        self.driver.find_element(By.ID, "LastName").send_keys(last)
        self.driver.find_element(By.ID, "Email").send_keys(email)
        self.driver.find_element(By.ID, "Password").send_keys(password)
        self.driver.find_element(By.ID, "ConfirmPassword").send_keys(password)

        btn = self.driver.find_element(By.ID, "register-button")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        self.driver.execute_script("arguments[0].click();", btn)

        msg = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "result"))
        ).text

        return msg
