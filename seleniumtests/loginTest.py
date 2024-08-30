from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

driver.get("http://127.0.0.1:8000/main/")

driver.find_element(By.LINK_TEXT,"Login").click()
driver.implicitly_wait(0.5)
url = driver.current_url
assert url == "http://127.0.0.1/main/login/"

driver.quit()
