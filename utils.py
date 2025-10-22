# utils.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from openpyxl import load_workbook
import os

def create_driver(browser="chrome", headless=True):
    """
    Create a webdriver instance for Chrome or Firefox with CI-friendly options.
    headless=True by default (good for GitHub Actions).
    """
    browser = browser.lower()

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            # Use new headless if available; fallback to classic if not
            try:
                options.add_argument("--headless=new")
            except Exception:
                options.add_argument("--headless")
        # CI friendly flags
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-sync")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--metrics-recording-only")
        options.add_argument("--mute-audio")
        # Ensure a writable user data dir (important on GitHub runner)
        tmp_profile = "/tmp/.chrome-profile-{}".format(os.getpid())
        os.makedirs(tmp_profile, exist_ok=True)
        options.add_argument(f"--user-data-dir={tmp_profile}")
        # optional: reduce automation detection
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(60)
        return driver

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        # firefox specific flags
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)

        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_page_load_timeout(60)
        return driver

    else:
        raise ValueError(f"Unsupported browser: {browser}")


# ---------- Excel reader (unchanged) ----------
def read_excel(path, sheet="Sheet1"):
    wb = load_workbook(path)
    ws = wb[sheet]
    rows = list(ws.values)
    if not rows:
        return []
    headers = rows[0]
    data = []
    for r in rows[1:]:
        # make sure to handle uneven rows
        row_dict = {}
        for i, h in enumerate(headers):
            if i < len(r):
                row_dict[h] = r[i]
            else:
                row_dict[h] = None
        data.append(row_dict)
    return data
