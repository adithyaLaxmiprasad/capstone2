import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import shutil
import os

def get_driver_for(browser: str, headless: bool = False):
    """
    Always use Chromium in GitHub Actions
    (Chrome 142 has bugs on Windows CI).
    """
    if browser.lower() == "chrome":
        opts = ChromeOptions()

        # Location of Chromium on Windows GitHub Action runner
        opts.binary_location = r"C:\Program Files (x86)\Chromium\Application\chromium.exe"

        if headless:
            opts.add_argument("--headless=new")

        opts.add_argument("--disable-gpu")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--window-size=1920,1080")

        return webdriver.Chrome(options=opts)

    raise ValueError("Only Chrome/Chromium supported")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store_true", default=False)


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
            allure.attach(png, name=f"screenshot-{request.node.name}",
                           attachment_type=allure.attachment_type.PNG)
        except:
            pass

    drv.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
