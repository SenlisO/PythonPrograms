#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

# flags
headless_flag = True

# set up the firefox webdriver
browser_options = Options()

if (headless_flag):
    browser_options.add_argument('-headless')

browser = webdriver.Firefox(firefox_options=browser_options)
wait = WebDriverWait(browser, timeout=10)

# go to login screen, fill out username and password, and sub
print("logging in to GCI")

browser.get('https://login.gci.com/#quick-link')
user_elem = browser.find_element_by_id('username')
user_elem.send_keys("Senlis")
pass_elem = browser.find_element_by_id('password')
pass_elem.send_keys("[Redacted]")
login_button = browser.find_element_by_id('login')
login_button.click()

# now, go to usage screen
print("navigating to GCI data usage screen")
browser.get('https://apps.gci.com/um/overview#quick-link')

# identify web elements
wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'total')))
wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'cap')))
wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'days')))
print("collecting data")
usage_elem = browser.find_element_by_class_name('total')
total_elem = browser.find_element_by_class_name('cap')
days_elem = browser.find_element_by_class_name('days')

# collect data from elements
GCI_data_usage = float(usage_elem.text)
GCI_total_data = float(total_elem.text)
temp_string = days_elem.text
split_string = str.split(temp_string)  # default is to split string by spaces
GCI_days_into_period = 30 - int(split_string[0])
if GCI_days_into_period < 0:  # just in case billing period is 31 days long
    GCI_days_into_period = 0  # we will just round up

# perform calculations on data usage
GCI_percentage_used = int((GCI_data_usage / GCI_total_data) * 100)
GCI_percentage_into_period = int((GCI_days_into_period / 30) * 100)  # assumed all billing periods are 30 days long
print("GCI data collected")
print("-----------------------------------------------")

# navigate to AT&T
print("logging into AT&T")
browser.get('https://www.att.com/my/#/login')
wait.until(expected.visibility_of_element_located((By.ID, 'userName')))
wait.until(expected.visibility_of_element_located((By.ID, 'password')))
user_elem = browser.find_element_by_id('userName')
user_elem.send_keys("gizmo.romick@gmail.com")
pass_elem = browser.find_element_by_id('password')
pass_elem.send_keys("[Redacted]")
login_button = browser.find_element_by_id('loginButton')
login_button.click()

# identify web elements
wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, '.cboDaysLeft')))
wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, 'div.usage-bar:nth-child(3) > div:nth-child(1) > span:nth-child(1)')))
print("collecting data")
days_elem = browser.find_element_by_css_selector('.cboDaysLeft')
usage_elem = browser.find_element_by_css_selector('div.usage-bar:nth-child(3) > div:nth-child(1) > span:nth-child(1)')

# collect data from elements
split_string = str.split(usage_elem.text)  # default is to split string by spaces
ATT_data_usage = float(split_string[0])
ATT_total_data = float(split_string[2])
split_string = str.split(days_elem.text)  # default is to split string by spaces
ATT_days_into_period = 30 - int(split_string[0])
if ATT_days_into_period < 0:  # just in case billing period is 31 days long
    ATT_days_into_period      # we will just round up

# perform calculations on data usage
ATT_percentage_used = int((ATT_data_usage / ATT_total_data) * 100)
ATT_percentage_into_period = int((ATT_days_into_period / 30) * 100)  # assumed all billing periods are 30 days long
print("ATT data collected")

# print GCI data
print("--------------------------------------------------------------")
print("GCI data")
print("Data used: " + str(GCI_data_usage) + " of " + str(GCI_total_data))
print("Days into billing period: " + str(GCI_days_into_period) + " of 30")
print("Data percentage: " + str(GCI_percentage_used) + "%")
print("Percent into billing period: " + str(GCI_percentage_into_period) + "%")

# print ATT data
print("--------------------------------------------------------------")
print("AT&T data")
print("Data used: " + str(ATT_data_usage) + " of " + str(ATT_total_data))
print("Days into billing period: " + str(ATT_days_into_period) + " of 30")
print("Data percentage: " + str(ATT_percentage_used) + "%")
print("Percent into billing period: " + str(ATT_percentage_into_period) + "%")
