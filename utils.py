# utils.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from openpyxl import load_workbook

def create_driver(browser="chrome"):
    if browser.lower() == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service)
    elif browser.lower() == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

# Excel reader remains the same
def read_excel(path, sheet="Sheet1"):
    wb = load_workbook(path)
    ws = wb[sheet]
    rows = list(ws.values)
    if not rows:
        return []
    headers = rows[0]
    data = []
    for r in rows[1:]:
        data.append({headers[i]: r[i] for i in range(len(headers))})
    return data
