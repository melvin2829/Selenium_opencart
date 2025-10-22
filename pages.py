# pages.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time

class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def find_visible(self, by, locator):
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    def click(self, by, locator):
        el = self.find_visible(by, locator)
        el.click()

    def type(self, by, locator, text, retries=3):
        """Safe send_keys with retry in case of StaleElementReferenceException."""
        for attempt in range(retries):
            try:
                el = self.find_visible(by, locator)
                el.clear()
                el.send_keys(text)
                return
            except StaleElementReferenceException:
                time.sleep(1)
        # last try
        el = self.find_visible(by, locator)
        el.clear()
        el.send_keys(text)

    def js_click(self, by, locator):
        el = self.find_visible(by, locator)
        self.driver.execute_script("arguments[0].click();", el)

    def hover(self, el):
        ActionChains(self.driver).move_to_element(el).perform()


class HomePage(BasePage):
    SEARCH = (By.NAME, "search")       # locator for search box
    SEARCH_BTN = (By.CSS_SELECTOR, "button.btn.btn-default.btn-lg")  # search button

    def search(self, term):
        """Search for a product using the search bar."""
        self.type(*self.SEARCH, term)
        self.click(*self.SEARCH_BTN)


class LoginPage(BasePage):
    LOGIN_MENU = (By.LINK_TEXT, "My Account")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    EMAIL = (By.ID, "input-email")
    PASSWORD = (By.ID, "input-password")
    LOGIN_BTN = (By.CSS_SELECTOR, "input[value='Login']")

    def open_login(self):
        self.click(*self.LOGIN_MENU)
        self.click(*self.LOGIN_LINK)

    def login(self, username, password):
        self.type(*self.EMAIL, username)
        self.type(*self.PASSWORD, password)
        self.click(*self.LOGIN_BTN)
        time.sleep(2)  # wait for page to stabilize after login


class ProductPage(BasePage):
    ADD_TO_CART = (By.ID, "button-cart")

    def add_to_cart(self):
        self.click(*self.ADD_TO_CART)


class CartPage(BasePage):
    CART_BUTTON = (By.ID, "cart")
    VIEW_CART = (By.LINK_TEXT, "View Cart")

    def open_cart(self):
        self.click(*self.CART_BUTTON)
        self.click(*self.VIEW_CART)
