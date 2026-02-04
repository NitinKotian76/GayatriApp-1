from selenium import webdriver
from selenium.webdriver.common.by import By


def login(base_url: str = "http://127.0.0.1:8000") -> None:
    """Basic smoke test: user can log in and reach the index page."""
    driver = webdriver.Firefox()
    try:
        driver.get(f"{base_url}/main/")

        driver.find_element(By.LINK_TEXT, "Login").click()
        driver.implicitly_wait(1)
        assert driver.current_url.rstrip("/") == f"{base_url}/main/login"

        username = driver.find_element(By.NAME, value="Username")  # employee code
        password = driver.find_element(By.NAME, value="Password")
        company = driver.find_element(By.NAME, value="select*Company")
        login_button = driver.find_element(By.NAME, value="Login")

        # NOTE: credentials and company must exist in the local dev database
        username.send_keys("01")
        password.send_keys("testpassword")
        company.send_keys("UNIT 2")
        login_button.click()
        driver.implicitly_wait(1)

        assert driver.current_url.rstrip("/") == f"{base_url}/main/index"
    finally:
        driver.quit()


if __name__ == "__main__":
    login()
