# tests/test_e2e.py
import pytest
from utils import read_excel
from pages import HomePage, LoginPage, ProductPage, CartPage

# Load test data at module import so pytest can parametrize
TESTDATA = read_excel("testdata.xlsx", sheet="Sheet1")  # returns list of dicts

# Optional: sanity check
if not TESTDATA:
    raise RuntimeError("No test data found in testdata.xlsx (Sheet1). Please add rows.")

@pytest.mark.parametrize("row", TESTDATA)
def test_login_search_add_cart_logout(driver, row):
    """
    Parametrized E2E test — runs once per Excel row (row is a dict with keys: username, password, search_term)
    """
    home = HomePage(driver)
    login = LoginPage(driver)
    product = ProductPage(driver)
    cart = CartPage(driver)

    # Login
    login.open_login()
    login.login(row["username"], row["password"])

    # Search and add product
    home.search(row["search_term"])
    product.open_first()
    product.add_to_cart()

    # Open cart and assert product presence
    cart.open_cart()
    assert cart.has_product(row["search_term"]), f"{row['search_term']} not found in cart for {row['username']}"

    # Logout (try-safe)
    try:
        # using By.LINK_TEXT pattern may vary by site; this is a generic attempt
        driver.find_element("link text", "Sign out").click()
    except Exception:
        try:
            driver.find_element("link text", "Logout").click()
        except Exception:
            pass
