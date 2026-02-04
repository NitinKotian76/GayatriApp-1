from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


BASE_URL = "http://127.0.0.1:8000"
TEST_USER_CODE = "01"
TEST_USER_PASSWORD = "testpassword"


def _login_as_test_user(driver: WebDriver) -> None:
    """
    Log in using the provided test user credentials so that the
    non-admin (user) navigation is rendered.
    """
    driver.get(f"{BASE_URL}/main/")

    driver.find_element(By.LINK_TEXT, "Login").click()
    driver.implicitly_wait(1)

    emp_code_input = driver.find_element(By.NAME, value="Username")
    password_input = driver.find_element(By.NAME, value="Password")
    login_button = driver.find_element(By.NAME, value="Login")

    emp_code_input.send_keys(TEST_USER_CODE)
    password_input.send_keys(TEST_USER_PASSWORD)
    login_button.click()
    driver.implicitly_wait(1)


def _open_dropdown(driver: WebDriver, button_text: str) -> None:
    """
    Click the dropdown button in usernav.html by visible text
    (e.g. 'Transaction', 'Report', 'Utility').
    """
    button = driver.find_element(
        By.XPATH,
        f"//div[contains(@class, 'w3-dropdown-hover')]"
        f"/a[contains(normalize-space(.), '{button_text}')]",
    )
    button.click()
    driver.implicitly_wait(1)


def _assert_menu_item(
    driver: WebDriver,
    parent_label: str,
    item_text: str,
    expected_hx_get: str,
    expected_hx_vals: str | None = None,
) -> None:
    """
    Within a given dropdown, assert that an entry has the expected
    hx-get (and optionally hx-vals) attributes. This ties the visible
    menu to the underlying URLs and form identifiers.
    """
    _open_dropdown(driver, parent_label)

    item = driver.find_element(
        By.XPATH,
        "//div[contains(@class, 'w3-dropdown-content')]"
        f"//a[normalize-space(.)='{item_text}']",
    )
    hx_get_value = item.get_attribute("hx-get")
    assert (
        hx_get_value == expected_hx_get
    ), f"{item_text} hx-get expected {expected_hx_get!r}, got {hx_get_value!r}"

    if expected_hx_vals is not None:
        hx_vals_value = item.get_attribute("hx-vals")
        assert (
            hx_vals_value == expected_hx_vals
        ), f"{item_text} hx-vals expected {expected_hx_vals!r}, got {hx_vals_value!r}"


def test_user_navigation_links() -> None:
    """
    Selenium smoke test for the regular user's navigation (usernav.html).

    Logs in as the test user (emp code 01) and verifies that key nav
    entries point at the expected URLs and form identifiers. This will
    fail if URLs or hx-vals are changed without updating the nav.
    """
    driver = webdriver.Firefox()
    try:
        _login_as_test_user(driver)

        # Transaction dropdown
        _assert_menu_item(
            driver,
            parent_label="Transaction",
            item_text="Opening balance Production",
            expected_hx_get="/invoice/form_view",
            expected_hx_vals='{"form":"open_bal_prod"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Transaction",
            item_text="Production",
            expected_hx_get="/invoice/tproduction/create",
            expected_hx_vals='{"form":"production"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Transaction",
            item_text="Stock Plus/minus",
            expected_hx_get="/invoice/tproduction",
            expected_hx_vals='{"form":"prod_plus_minus"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Transaction",
            item_text="Production Approval",
            expected_hx_get="/invoice/form_view",
            expected_hx_vals='{"form":"prod_approval"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Transaction",
            item_text="Invoice",
            expected_hx_get="/invoice/tinvoice/create",
            expected_hx_vals='{"form":"invoice"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Transaction",
            item_text="Jumbo Roll QC",
            expected_hx_get="/invoice/tjumborollwiseqc/create",
        )
        # NOTE: URLconf uses `tlotnowiseqc`, so this assertion ensures the
        # template link stays consistent with that path.
        _assert_menu_item(
            driver,
            parent_label="Transaction",
            item_text="LOT no Wise QC",
            expected_hx_get="/invoice/tlotnowiseqc/create",
            expected_hx_vals='{"form":"lot_no_wise_qc"}',
        )

        # Report dropdown
        _assert_menu_item(
            driver,
            parent_label="Report",
            item_text="Pending Order",
            expected_hx_get="/invoice/report_view",
            expected_hx_vals='{"form":"pending_order"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Report",
            item_text="Production Record",
            expected_hx_get="/invoice/report_view",
            expected_hx_vals='{"form":"prod_record"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Report",
            item_text="Dispatch Details",
            expected_hx_get="/invoice/report_view",
            expected_hx_vals='{"form":"dispatch_details"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Report",
            item_text="Stock",
            expected_hx_get="/invoice/report_view",
            expected_hx_vals='{"form":"stock"}',
        )

        # Utility dropdown
        _assert_menu_item(
            driver,
            parent_label="Utility",
            item_text="API",
            expected_hx_get="/invoice/form_view",
            expected_hx_vals='{"form":"api"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Utility",
            item_text="Multiple Export Packing Slip",
            expected_hx_get="/invoice/form_view",
            expected_hx_vals='{"form":"multiple_export_packing_slip"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Utility",
            item_text="MillSoft To Orion",
            expected_hx_get="/invoice/form_view",
            expected_hx_vals='{"form":"millsoft_to_orion"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Utility",
            item_text="Backup",
            expected_hx_get="/invoice/form_view",
            expected_hx_vals='{"form":"backup"}',
        )
        _assert_menu_item(
            driver,
            parent_label="Utility",
            item_text="Printer Setting",
            expected_hx_get="/invoice/form_view",
        )
        _assert_menu_item(
            driver,
            parent_label="Utility",
            item_text="Calculator",
            expected_hx_get="/invoice/form_view",
            expected_hx_vals='{"form":"printer_setting"}',
        )
    finally:
        driver.quit()


if __name__ == "__main__":
    test_user_navigation_links()

