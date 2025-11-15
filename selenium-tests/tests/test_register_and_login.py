# selenium-tests/tests/test_register_and_login.py
import pytest, time
from pages.register_page import RegisterPage

def test_register_and_login(driver, base_url):
    register = RegisterPage(driver, base_url)
    register.open()
    ts = int(time.time())
    email = f"testuser{ts}@example.com"
    msg = register.register("Test", "User", email, "Pass@1234")
    assert "Your registration completed" in msg
    # Optionally test login link separately if you have LoginPage implemented
