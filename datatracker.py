#!/usr/bin/python3
from selenium import webdriver
import time
import smtplib  # email module

# set up the firefox webdriver
browser = webdriver.Firefox()

# go to login screen, fill out username and password, and sub
browser.get('https://login.gci.com/#quick-link')
user_elem = browser.find_element_by_id('username')
user_elem.send_keys("Senlis")
pass_elem = browser.find_element_by_id('password')
pass_elem.send_keys('[REDACTED]')
# pass_elem.submit()   this does not seem to work well
login_button = browser.find_element_by_id('login')
login_button.click()

# now, go to usage screen
browser.get('https://apps.gci.com/um/overview#quick-link')

# print data usage
time.sleep(5)
usage_elem = browser.find_element_by_class_name('total')
print(usage_elem.text)
days_elem = browser.find_element_by_class_name('days')
print(days_elem.text)

# send our message with all the data
with smtplib.SMTP('smtp.gmail.com', 587) as smtp_object:  # this opens an smtp object that exists within the indented block
    smtp_object.starttls()
    smtp_object.login('gizmocomputerservices@gmail.com', '[REDACTED]')
    message_body = "Subject: Data Usage Report\n\n" + "Total data usage: " + usage_elem.text + "\nDays into billing cycle " + days_elem.text
    print('message body: ' + message_body)
    smtp_object.sendmail('gizmocomputerservices@gmail.com', 'gizmo.romick@gmail.com', message_body)
