# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestSignout():
  def setup_method(self, method):
    self.driver = webdriver.Chrome(executable_path='C:\Driver\chromedriver.exe')
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_signout(self):
    # Test name: signout
    # Step # | name | target | value
    # 1 | open | http://127.0.0.1:8000/login/?next=/customerView/ | 
    self.driver.get("http://127.0.0.1:8000/login/?next=/customerView/")
    # 2 | setWindowSize | 1536x864 | 
    self.driver.set_window_size(1536, 864)
    # 3 | type | id=id_username | Brayan@gmail.com
    self.driver.find_element(By.ID, "id_username").send_keys("Brayan@gmail.com")
    # 4 | type | id=id_password | Lemu$123
    self.driver.find_element(By.ID, "id_password").send_keys("Lemu$123")
    # 5 | sendKeys | id=id_password | ${KEY_ENTER}
    self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
    # 6 | click | linkText=Sign Out | 
    self.driver.find_element(By.LINK_TEXT, "Sign Out").click()
  
