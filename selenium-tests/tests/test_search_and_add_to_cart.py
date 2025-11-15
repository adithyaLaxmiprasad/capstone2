import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage

def test_search_and_add_to_cart(driver, base_url):
    home = HomePage(driver, base_url)   # must accept (driver, base_url)
    home.open()

    # Search
    home.search("laptop")

    # Wait for results page to load and open first product
    sr = SearchResultsPage(driver)
    first_title = sr.first_product_title()
    sr.open_first_product()

    # Product page: validate title & add to cart
    pp = ProductPage(driver)
    assert first_title in pp.get_title()
    pp.add_to_cart()

    # Wait until cart quantity updates to >= 1 (no time.sleep)
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: home.cart_quantity() >= 1)

    assert home.cart_quantity() >= 1
