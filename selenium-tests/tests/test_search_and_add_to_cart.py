from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage

def test_search_and_add_to_cart(driver, base_url):
    home = HomePage(driver, base_url)
    home.open()

    home.search("laptop")

    sr = SearchResultsPage(driver)
    title = sr.first_product_title()
    sr.open_first_product()

    pp = ProductPage(driver)
    assert title in pp.get_title()
