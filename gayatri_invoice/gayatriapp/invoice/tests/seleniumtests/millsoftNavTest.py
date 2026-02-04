from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


BASE_URL = "http://127.0.0.1:8000"


def _login(driver: WebDriver) -> None:
    """Log in using the existing login page so Millsoft menus are available."""
    driver.get(f"{BASE_URL}/main/")

    driver.find_element(By.LINK_TEXT, "Login").click()
    driver.implicitly_wait(1)

    username = driver.find_element(By.NAME, value="Username")
    password = driver.find_element(By.NAME, value="Password")
    login_button = driver.find_element(By.NAME, value="Login")

    username.send_keys("nixon")
    password.send_keys("nixon")
    login_button.click()
    driver.implicitly_wait(1)


def _assert_hx_get(driver: WebDriver, link_text: str, expected_hx_get: str) -> None:
    """
    Open the admin navigation dropdown and assert that the entry with the given
    visible text points to the expected hx-get URL.

    This verifies that the UI navigation remains in sync with the Django URLs.
    """
    # Open the "Masters" dropdown (adminnav.html)
    masters_button = driver.find_element(
        By.XPATH, "//a[contains(normalize-space(.), 'Masters')]"
    )
    masters_button.click()
    driver.implicitly_wait(1)

    entry = driver.find_element(
        By.XPATH,
        f"//div[contains(@class, 'w3-dropdown-content')]"
        f"//a[normalize-space(.)='{link_text}']",
    )
    hx_get_value = entry.get_attribute("hx-get")
    assert (
        hx_get_value == expected_hx_get
    ), f"{link_text} hx-get expected {expected_hx_get!r}, got {hx_get_value!r}"


def test_millsoft_master_navigation() -> None:
    """
    Selenium smoke test for Millsoft master navigation.

    For each active master module, confirm that the menu entry points to the
    correct Django URL via its hx-get attribute.
    """
    driver = webdriver.Firefox()
    try:
        _login(driver)

        # Agent
        _assert_hx_get(driver, "Agent", "/invoice/magent/create")
        # Customer
        _assert_hx_get(driver, "customer", "/invoice/mcustomer/create")
        # Supplier
        _assert_hx_get(driver, "Supplier", "/invoice/msupplier/create")
        # Export
        _assert_hx_get(driver, "Export", "/invoice/mexportfields/create")
        # Category
        _assert_hx_get(driver, "Category", "/invoice/mcategory/create")
        # Shade/Variety
        _assert_hx_get(driver, "Shade/Variety", "/invoice/mshade/create")
        # Item Name
        _assert_hx_get(driver, "Item Name", "/invoice/mitem/create")
        # Stock Plus minus head
        _assert_hx_get(
            driver, "Stock Plus minus head", "/invoice/mplusminushead/create"
        )
        # Location
        _assert_hx_get(driver, "Location", "/invoice/mlocation/create")
    finally:
        driver.quit()


if __name__ == "__main__":
    test_millsoft_master_navigation()

