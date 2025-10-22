# pages.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def find_all(self, by, locator):
        return self.wait.until(EC.presence_of_all_elements_located((by, locator)))

    def click(self, by, locator):
        self.find(by, locator).click()

    def type(self, by, locator, text):
        el = self.find(by, locator)
        el.clear()
        el.send_keys(text)

    def js_click(self, by, locator):
        el = self.find(by, locator)
        self.driver.execute_script("arguments[0].click();", el)

    def hover(self, el):
        ActionChains(self.driver).move_to_element(el).perform()

class HomePage(BasePage):
    SEARCH = (By.NAME, "search")
    SEARCH_BTN = (By.CSS_SELECTOR, "div#search button")

    def search(self, term):
        self.type(*self.SEARCH, term)
        self.click(*self.SEARCH_BTN)

class LoginPage(BasePage):
    MY_ACCOUNT = (By.XPATH, "//a[@title='My Account']")
    LOGIN = (By.LINK_TEXT, "Login")
    EMAIL = (By.ID, "input-email")
    PASSWORD = (By.ID, "input-password")
    LOGIN_BTN = (By.CSS_SELECTOR, "input[type='submit'][value='Login']")

    def open_login(self):
        self.click(*self.MY_ACCOUNT)
        self.click(*self.LOGIN)

    def login(self, email, pwd):
        self.type(*self.EMAIL, email)
        self.type(*self.PASSWORD, pwd)
        self.click(*self.LOGIN_BTN)

class ProductPage(BasePage):
    FIRST_PRODUCT = (By.CSS_SELECTOR, "div.product-layout div.caption a")
    ADD_TO_CART = (By.ID, "button-cart")  # depends on page

    def open_first(self):
        self.click(*self.FIRST_PRODUCT)

    def add_to_cart(self):
        self.click(*self.ADD_TO_CART)

class CartPage(BasePage):
    CART_BUTTON = (By.ID, "cart")           # quick view
    VIEW_CART = (By.LINK_TEXT, "View Cart") # open cart page
    TABLE_ROWS = (By.CSS_SELECTOR, "table.table tbody tr")

    def open_cart(self):
        self.click(*self.CART_BUTTON)
        # sometimes need to click view cart
        try:
            self.click(*self.VIEW_CART)
        except:
            pass

    def has_product(self, name):
        rows = self.find_all(*self.TABLE_ROWS)
        return any(name.lower() in r.text.lower() for r in rows)
