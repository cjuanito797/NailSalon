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

class TestSignup():
  def setup_method(self, method):
    self.driver = webdriver.Chrome(executable_path='C:\Driver\chromedriver.exe')
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_signup(self):
    self.driver.get("http://127.0.0.1:8000/registration/")
    self.driver.set_window_size(1552, 880)
    self.driver.find_element(By.ID, "id_email").send_keys("lemus@gmail.com")
    self.driver.find_element(By.ID, "id_password1").send_keys("Lemus@123")
    self.driver.find_element(By.ID, "id_password2").send_keys("Lemus@123")
    self.driver.find_element(By.ID, "id_first_name").send_keys("Brayan")
    self.driver.find_element(By.ID, "id_last_name").send_keys("Lemus")
    self.driver.find_element(By.ID, "id_street_num").send_keys("1255444")
    self.driver.find_element(By.ID, "id_city").send_keys("Omaha")
    self.driver.find_element(By.ID, "id_state").click()
    dropdown = self.driver.find_element(By.ID, "id_state")
    dropdown.find_element(By.XPATH, "//option[. = 'Nebraska']").click()
    self.driver.find_element(By.ID, "id_zipcode").click()
    self.driver.find_element(By.ID, "id_zipcode").send_keys("64165")
    self.driver.find_element(By.ID, "id_phoneNumber").send_keys("4654654654")
    self.driver.find_element(By.CSS_SELECTOR, ".is-block").click()
  
