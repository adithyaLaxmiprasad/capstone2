import uuid
import time
from pages.register_page import RegisterPage
from pages.login_page import LoginPage


def test_register_and_login(driver, base_url):
    register = RegisterPage(driver, base_url)
    register.open()

    # Always unique email
    email = f"testuser_{uuid.uuid4().hex}@example.com"
    password = "Pass@1234"

    # Step 1: Register a new user
    msg = register.register("Test", "User", email, password)
    assert "Your registration completed" in msg

    # Step 2: Now log in with the same user
    login = LoginPage(driver, base_url)
    login.open()

    login_success = login.login(email, password)
    assert "My account" in login_success  # or assert login_success == True
