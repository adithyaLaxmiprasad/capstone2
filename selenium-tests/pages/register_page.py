from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class RegisterPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = f"{base_url}register"

    def open(self):
        self.driver.get(self.url)

        # Close cookie popup if shown
        try:
            cookie_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, "eu-cookie-ok"))
            )
            self.driver.execute_script("arguments[0].click();", cookie_btn)
        except:
            pass

    def register(self, first_name, last_name, email, password):

        # ---- Required field: Gender ----
        try:
            self.driver.find_element(By.ID, "gender-male").click()
        except:
            pass

        # ---- Required field: Date of Birth ----
        try:
            Select(self.driver.find_element(By.NAME, "DateOfBirthDay")).select_by_value("1")
            Select(self.driver.find_element(By.NAME, "DateOfBirthMonth")).select_by_value("1")
            Select(self.driver.find_element(By.NAME, "DateOfBirthYear")).select_by_value("1990")
        except:
            pass

        # Fill fields
        self.driver.find_element(By.ID, "FirstName").send_keys(first_name)
        self.driver.find_element(By.ID, "LastName").send_keys(last_name)
        self.driver.find_element(By.ID, "Email").send_keys(email)
        self.driver.find_element(By.ID, "Password").send_keys(password)
        self.driver.find_element(By.ID, "ConfirmPassword").send_keys(password)

        register_btn = self.driver.find_element(By.ID, "register-button")

        # Scroll into view (headless fix)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", register_btn
        )

        # Try normal click → fallback to JS click
        try:
            register_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", register_btn)

        # Wait for the success message
        msg = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "result"))
        ).text

        return msg
