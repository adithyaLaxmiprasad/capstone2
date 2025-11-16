import pytest
import allure
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.chrome.service import Service
import time


def get_driver_for(headless=False):
    """Always use Edge in CI (stable and pre-installed)."""

    opts = EdgeOptions()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")

    # Edge + Selenium auto-detects driver (works in GitHub Actions)
    return webdriver.Edge(options=opts)


def pytest_addoption(parser):
    parser.addoption("--browser", default="edge")
    parser.addoption("--headless", action="store_true")


@pytest.fixture(scope="session")
def base_url():
    return "https://demo.nopcommerce.com/"


@pytest.fixture(scope="function")
def driver(request):
    headless = request.config.getoption("--headless")

    drv = get_driver_for(headless=headless)
    drv.implicitly_wait(10)

    yield drv

    # Attach screenshot on failure
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        try:
            png = drv.get_screenshot_as_png()
            allure.attach(png, name="failure-screenshot",
                          attachment_type=allure.attachment_type.PNG)
        except:
            pass

    drv.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
