import os

BASE_URL = os.getenv("BASE_URL", "https://demo.nopcommerce.com/")
ADMIN_URL = os.getenv("ADMIN_URL", "https://admin-demo.nopcommerce.com/")  # if using admin interface
DEFAULT_BROWSER = os.getenv("BROWSER", "chrome")  # chrome | firefox | edge
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "10"))
HEADLESS = os.getenv("HEADLESS", "false").lower() in ("1","true","yes")
ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")
# Admin credentials - ALWAYS put real secrets into CI env vars, not in repo
ADMIN_USER = os.getenv("ADMIN_USER", "admin@yourdomain.com")
ADMIN_PASS = os.getenv("ADMIN_PASS", "adminpassword")
