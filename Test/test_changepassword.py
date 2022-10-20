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

class TestChangePassword():
  def setup_method(self, method):
    self.driver = webdriver.Chrome(executable_path='C:\Driver\chromedriver.exe')
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_changePassword(self):
    # Test name: Change Password
    # Step # | name | target | value
    # 1 | open | http://127.0.0.1:8000/login/ | 
    self.driver.get("http://127.0.0.1:8000/login/")
    # 3 | type | id=id_username | Brayan@gmail.com
    self.driver.find_element(By.ID, "id_username").send_keys("Brayan@gmail.com")
    # 4 | type | id=id_password | Br@yan123
    self.driver.find_element(By.ID, "id_password").send_keys("Br@yan123")

    # 6 | open | http://127.0.0.1:8000/customerView/ | 
    self.driver.get("http://127.0.0.1:8000/customerView/")
    # 7 | mouseOver | linkText=My Account | 
    element = self.driver.find_element(By.LINK_TEXT, "My Account")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    # 8 | click | linkText=My Profile | 
    self.driver.find_element(By.LINK_TEXT, "My Profile").click()
    # 9 | click | linkText=Change Password | 
    self.driver.find_element(By.LINK_TEXT, "Change Password").click()
    # 10 | click | id=id_old_password | 
    self.driver.find_element(By.ID, "id_old_password").click()
    # 11 | type | id=id_old_password | Br@yan123
    self.driver.find_element(By.ID, "id_old_password").send_keys("Br@yan123")
    # 12 | type | id=id_new_password1 | Lemu$123
    self.driver.find_element(By.ID, "id_new_password1").send_keys("Lemu$123")
    # 13 | type | id=id_new_password2 | Lemu$123
    self.driver.find_element(By.ID, "id_new_password2").send_keys("Lemu$123")
    # 14 | click | css=.is-block | 
    self.driver.find_element(By.CSS_SELECTOR, ".is-block").click()
    # 15 | open | http://127.0.0.1:8000/login/ | 
    self.driver.get("http://127.0.0.1:8000/login/")
    # 16 | click | id=id_username | 
    self.driver.find_element(By.ID, "id_username").click()
    # 17 | type | id=id_username | Brayan@gmail.com
    self.driver.find_element(By.ID, "id_username").send_keys("Brayan@gmail.com")
    # 18 | type | id=id_password | Lemu$123
    self.driver.find_element(By.ID, "id_password").send_keys("Lemu$123")

  
