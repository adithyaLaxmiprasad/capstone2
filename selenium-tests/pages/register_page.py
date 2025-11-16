# selenium-tests/pages/register_page.py

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

        register_btn = self.driver.find_element(By.ID, "register-button")

        # ---- CI FIX: ensure visibility on headless browser ----
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", register_btn
        )

        # Try normal click; fallback to JS click if needed
        try:
            register_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", register_btn)

        msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "result"))
        ).text

        return msg
