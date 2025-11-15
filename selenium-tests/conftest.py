# selenium-tests/conftest.py
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
import shutil
import os

def get_driver_for(browser: str, headless: bool = False):
    """
    Return a WebDriver instance for the requested browser.
    Keep this simple — if you need special Service paths, edit here.
    """
    if browser.lower() == "chrome":
        opts = ChromeOptions()
        if headless:
            # new headless flag for recent Chrome versions
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        # optionally: opts.add_argument("--disable-gpu")
        return webdriver.Chrome(options=opts)

    elif browser.lower() == "edge":
        opts = EdgeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        return webdriver.Edge(options=opts)

    else:
        raise ValueError("Unsupported browser. Use --browser chrome|edge")

# ------------- CLI options -------------
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests on: chrome or edge")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run browsers in headless mode")

# ------------- fixtures -------------
@pytest.fixture(scope="session")
def base_url():
    """Base URL used by tests (inject as fixture)."""
    return "https://demo.nopcommerce.com/"

@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def headless(request):
    return request.config.getoption("--headless")

@pytest.fixture(scope="function")
def driver(request, browser_name, headless):
    """
    Creates and yields a WebDriver. On teardown, quits driver.
    Also stores the test report info on the request.node via pytest_runtest_makereport hook.
    Tests expect a fixture named `driver` so keep this name.
    """
    drv = get_driver_for(browser_name, headless=headless)
    # implicit wait is ok for simple flows; explicit waits are preferred in pages
    drv.implicitly_wait(10)

    yield drv

    # Attach screenshot on failure (requires pytest_runtest_makereport to set rep_call)
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        try:
            png = drv.get_screenshot_as_png()
            allure.attach(png, name=f"screenshot-{request.node.name}", attachment_type=allure.attachment_type.PNG)
        except Exception:
            # best-effort; don't crash teardown
            pass

    drv.quit()

# ------------- pytest hook to expose test results to fixtures -------------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Attach the test report object to the test 'item' so fixtures can read outcome."""
    outcome = yield
    rep = outcome.get_result()
    # attach to the node for access in fixtures (e.g. in driver teardown)
    setattr(item, "rep_" + rep.when, rep)
