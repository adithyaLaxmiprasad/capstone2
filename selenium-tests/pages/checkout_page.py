# selenium-tests/conftest.py
import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

IS_CI = os.getenv("GITHUB_ACTIONS") == "true"


def get_driver_for(browser: str, headless: bool = False):
    """
    Create and return a WebDriver instance.
    Ensures stable behavior on CI by forcing headless + window-size.
    """

    # Force headless on CI
    if IS_CI:
        headless = True

    if browser.lower() == "chrome":
        opts = ChromeOptions()

        if headless:
            opts.add_argument("--headless=new")

        # ---- Critical CI stability options ----
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--start-maximized")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument("--disable-infobars")

        return webdriver.Chrome(options=opts)

    elif browser.lower() == "edge":
        opts = EdgeOptions()

        if headless:
            opts.add_argument("--headless=new")

        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--start-maximized")

        return webdriver.Edge(options=opts)

    else:
        raise ValueError("Unsupported browser. Use chrome or edge.")


# ------------- CLI options -------------
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser: chrome or edge")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run in headless mode")


# ------------- fixtures -------------
@pytest.fixture(scope="session")
def base_url():
    return "https://demo.nopcommerce.com/"


@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request):
    return request.config.getoption("--headless")


@pytest.fixture(scope="function")
def driver(request, browser_name, headless):
    drv = get_driver_for(browser_name, headless=headless)
    drv.implicitly_wait(10)
    yield drv

    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        try:
            png = drv.get_screenshot_as_png()
            allure.attach(
                png,
                name=f"screenshot-{request.node.name}",
                attachment_type=allure.attachment_type.PNG
            )
        except:
            pass

    drv.quit()


# -------- pytest hook for attaching result --------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
