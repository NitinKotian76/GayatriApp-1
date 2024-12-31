from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

driver.get("http://127.0.0.1:8000/main/")

driver.find_element(By.LINK_TEXT,"Login").click()
driver.implicitly_wait(0.5)
url = driver.current_url
assert url == "http://127.0.0.1:8000/main/login"

username= driver.find_element(By.NAME,value="Username")
password= driver.find_element(By.NAME,value="Password")
login= driver.find_element(By.NAME,value="Login")
username.send_keys("nixon")
password.send_keys("nixon")
login.click()
assert url == "http://127.0.0.1:8000/main/index"

# forms= driver.find_element(By.)

driver.quit()
