# selenium-tests/tests/test_guest_checkout.py
import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.order_confirmation_page import OrderConfirmationPage

# These credentials should be a test account on the demo site.
# Replace with valid test account or store in env / conftest.
TEST_USER_EMAIL = "testauto123@gmail.com"
TEST_USER_PASSWORD = "Test@12345"

def test_guest_checkout_flow(driver, base_url):
    # 1) Search product and add to cart
    home = HomePage(driver, base_url)
    home.open()
    home.search("laptop")

    sr = SearchResultsPage(driver)
    sr.open_first_product()

    pp = ProductPage(driver)
    pp.add_to_cart()

    # 2) Open cart and first checkout action
    cart = CartPage(driver)
    cart.open()
    cp = CheckoutPage(driver, base_url)
    cp.begin_checkout()

    # 3) Login during checkout (use test creds)
    cp.login_checkout(TEST_USER_EMAIL, TEST_USER_PASSWORD)

    # 4) Complete remaining checkout steps and confirm
    cp.complete_checkout_steps()

    # 5) Assert order confirmation
    conf = OrderConfirmationPage(driver)
    assert conf.wait_for_thankyou_page(), "Order confirmation page did not appear"
