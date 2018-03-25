'''
How to run script
Script designed to run on Python3
Requires selenium to be installed
to install selenium, run "pip3 install selenium"
You will also need geckodriver.  Get it here:
https://github.com/mozilla/geckodriver/releases
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


def login_to_GCI(browser):
    '''
    Function logs into GCI
    Parameters:
        browser: handle on Firefox browser instance
    '''
    # go to login screen, fill out username and password and then press login button
    print("logging in to GCI")

    browser.get('https://login.gci.com/#quick-link')
    user_elem = browser.find_element_by_id('username')
    user_elem.send_keys("Senlis")
    pass_elem = browser.find_element_by_id('password')
    pass_elem.send_keys("[REDACTED]")
    login_button = browser.find_element_by_id('login')
    login_button.click()

    print("login complete")


# flags
headless_flag = True  # headless means no visible browser window
data_gathered = False  # when we get the data from the page we need, this flag allows us to continue

# variable
count = 3  # used to monitor how many times we try to navigate to a page

# set up the firefox webdriver
browser_options = Options()

# this if statement controls whether the browser starts headless (no visible browser window)
if (headless_flag):
    browser_options.add_argument('-headless')

# create browser object
browser = webdriver.Firefox(firefox_options=browser_options)

# set default wait times
wait = WebDriverWait(browser, timeout=10)

login_to_GCI(browser)  # function will log in for us

# navigate to data usage screen
# tries twice in headless mode, and then restarts browser in normal mode
# to give user the chance to correct whatever is preventing the browser
# from navigating (some pop-up window most likely)
while not data_gathered:
    # now, go to usage screen
    print("navigating to GCI data usage screen")
    browser.get('https://apps.gci.com/um/overview#quick-link')

    # get handles on data usage data elements
    try:  # wait until we see the necessary data elements or pause for troubleshooting
        wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'total')))
        wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'cap')))
        wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'days')))
        print("collecting data")

        # identify data elements
        usage_elem = browser.find_element_by_class_name('total')
        total_elem = browser.find_element_by_class_name('cap')
        days_elem = browser.find_element_by_class_name('days')
        data_gathered = True
    except TimeoutException:  # for some reason we didn't find the data elements we were looking for
        print("GCI data usage page timeout.  Count=" + str(count))  # display error to console
        if count > 2:  # this decision allows us to try again for a total of two times
            count -= 1  # decriment count once
        elif count > 1:  # we have already tried twice
            count -= 1  # decriment count once
            # restart browser in non-headless mode so we can see what we are doing
            # set up the firefox webdriver
            browser_options = Options()

            # create browser object
            browser = webdriver.Firefox(firefox_options=browser_options)

            # set default wait times
            wait = WebDriverWait(browser, timeout=10)

            # we may need to log in again
            login_to_GCI(browser)
        else:
            # display error message
            print("Timeout occurred without finding necessary data")
            temp = input("Please fix error and press enter to continue")
            print("Re-navigating to data usage screen.  Apply necessary changes to script")

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

# wait until we see the username and password fields to appear
wait.until(expected.visibility_of_element_located((By.ID, 'userName')))
wait.until(expected.visibility_of_element_located((By.ID, 'password')))

# enter username and password and then press login button
user_elem = browser.find_element_by_id('userName')
user_elem.send_keys("gizmo.romick@gmail.com")
pass_elem = browser.find_element_by_id('password')
pass_elem.send_keys("[REDACTED]")
login_button = browser.find_element_by_id('loginButton')
login_button.click()
# after last command, selenium navigates to "https://m.att.com/my/#/accountOverview"

# prepare some variables for data scraping loop
data_gathered = False
count = 3

# identify web elements
try:
    wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, '.cboDaysLeft')))
    wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, 'div.usage-bar:nth-child(3) > div:nth-child(1) > span:nth-child(1)')))

    print("collecting data")
    days_elem = browser.find_element_by_css_selector('.cboDaysLeft')
    usage_elem = browser.find_element_by_css_selector('div.usage-bar:nth-child(3) > div:nth-child(1) > span:nth-child(1)')
except TimeoutException:  # for some reason, we didn't find the data elements we were looking for
    print("AT&T account details page timeount.  Count=" + str(count))  # display error to console
    if count > 2:  # this decision allows us to try again for a total of two times
        count -= 1
        browser.get('https://m.att.com/my/#/accountOverview')  # try to manually navigate to account overview
    elif count > 1:  # we have already tried twice, now restart browser in non-headless mode
        pass
    else:
        pass

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
