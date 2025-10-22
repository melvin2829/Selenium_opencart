# conftest.py
import pytest
import time
from utils import create_driver, read_excel

# -----------------------------
# Add command-line options
# -----------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome or firefox"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://opencart.abstracta.us/",
        help="Base URL for the tests"
    )

# -----------------------------
# Config fixture (session scope)
# -----------------------------
@pytest.fixture(scope="session")
def config(request):
    return {
        "browser": request.config.getoption("--browser"),
        "base_url": request.config.getoption("--base-url")  # Note: use dash, not underscore
    }

# -----------------------------
# WebDriver fixture
# -----------------------------
@pytest.fixture
def driver(request, config):
    """
    Initialize WebDriver based on browser option, maximize window, open base URL.
    Quits driver after test.
    """
    drv = create_driver(config["browser"])
    drv.maximize_window()
    drv.get(config["base_url"])
    drv.get(config["base_url"])
    time.sleep(5)  # wait 5 seconds for page to load and any bot checks
    yield drv
    drv.quit()

# -----------------------------
# Excel test data fixture
# -----------------------------
@pytest.fixture(scope="session")
def testdata():
    """
    Reads testdata.xlsx from project root, sheet named 'Sheet1'.
    Returns a list of dictionaries, each row is one dict.
    """
    return read_excel("testdata.xlsx", sheet="Sheet1")
