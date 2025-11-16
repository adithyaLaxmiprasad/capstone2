import uuid
from pages.register_page import RegisterPage

def test_register_only(driver, base_url):
    page = RegisterPage(driver, base_url)
    page.open()

    email = f"test_{uuid.uuid4().hex}@example.com"
    message = page.register("Test", "User", email, "Pass@1234")

    assert "Your registration completed" in message
