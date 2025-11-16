import uuid
from pages.register_page import RegisterPage

def test_register_only(driver, base_url):
    register = RegisterPage(driver, base_url)
    register.open()

    email = f"test_{uuid.uuid4().hex}@example.com"
    password = "Pass@1234"

    msg = register.register("Test", "User", email, password)

    assert "Your registration completed" in msg
