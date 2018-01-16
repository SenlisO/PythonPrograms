from selenium import webdriver

# set up the firefox webdriver
browser = webdriver.Firefox()

# go to login screen, fill out username and password, and sub
browser.get('https://login.gci.com/#quick-link')
user_elem = browser.find_element_by_id('username')
user_elem.send_keys("Senlis")
pass_elem = browser.find_element_by_id('password')
pass_elem.send_keys('REDACTED')
# pass_elem.submit()   this does not seem to work well
login_button = browser.find_element_by_id('login')
login_button.click()

# now, go to usage screen
browser.get('https://apps.gci.com/um/overview#quick-link')

# print data usage
#usage_elem = browser.find_element_by_class_name('total')
#print(usage_elem.text)
