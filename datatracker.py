'''
How to run script
Script designed to run on Python3
Requires selenium to be installed
to install selenium, run "pip3 install selenium"
You will also need geckodriver.  Get it here:
https://github.com/mozilla/geckodriver/releases

Of course, you can't really use this script since the
passwords have been redacted.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

GCI_password = "redacted"
ATT_password = "redacted"
headless_flag = True


def wait_for_login_page(browser, wait, GCI):
    '''
    Function waits for page to load and takes necessary action if it fails
    Parameters:
        browser: handle on Firefox browser instance
        wait: object used to have browser handle wait on HTML elements to appear
        GCI: boolean value.  If true, logging into GCI.  If False, logging into AT&T
    '''
    page_loaded = False  # keeps us trying to log in until we find username/password field
    count = 3  # eventually allows us to stop trying if we are still not successful

    while not page_loaded:
        if GCI:  # trying to log ingo GCI
            # navigate to GCI login page
            print("logging in to GCI")
            browser.get('https://login.gci.com/#quick-link')
        else:  # trying to log into AT&T
            # navigate to AT&T
            print("logging into AT&T")
            browser.get('https://www.att.com/my/#/login')

        try:
            # wait until we see the username and password fields to appear
            if GCI:  # GCI
                wait.until(expected.visibility_of_element_located((By.ID, 'username')))
                wait.until(expected.visibility_of_element_located((By.ID, 'password')))
            else:  # AT&T
                wait.until(expected.visibility_of_element_located((By.ID, 'userName')))
                wait.until(expected.visibility_of_element_located((By.ID, 'password')))

            page_loaded = True  # if both previous elements are found, exit while loop
        except TimeoutException:  # for some reason, we didn't find the username/password fields
            print("Login timeout exception.  Count=" + str(count))
            if count > 1:  # if we haven't tried more than twice
                count -= 1  # just try again
            elif count > 0:  # if we have tried twice, restart in headless mode
                count -= 1

                # restart browser instance in non-headless mode
                headless_flag = False
                browser, wait = create_browser_instance(headless_flag)
            else:  # we have tried 3 times, pause for user to fix issue
                # display error message and wait for user input
                print("Timeout occurred without finding necessary data")
                input("Please fix error and press enter to continue")
                print("Re-navigating to login screen.  Apply necessary changes to script")


def wait_for_data_page(browser, wait, GCI):
    '''
    Function waits for data page to load and takes necessary action if it fails
    Parameters:
        browser: handle on Firefox browser instance
        wait: object used to have browser handle wait on HTML elements to appear
        GCI: boolean value.  If true, logging into GCI.  If False, logging into AT&T
    '''
    page_loaded = False  # keeps us trying to log in until we find username/password field
    count = 3  # eventually allows us to stop trying if we are still not successful

    while not page_loaded:
        if GCI:  # trying to log ingo GCI
            # navigate to GCI data page
            print("Navigating to GCI data usage screen")
            browser.get('https://apps.gci.com/um/overview#quick-link')
        else:  # trying to log into AT&T
            # navigate to AT&T
            if count < 3:  # only need to do this the second and third times
                browser.get('https://www.att.com/my/#/accountOverview')
            print("Logged into AT&T, waiting for data elements")

        try:
            # wait until we see the username and password fields to appear
            if GCI:  # GCI
                wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'total')))
                wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'cap')))
                wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'days')))
            else:  # AT&T
                wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, '.cboDaysLeft')))
                wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, 'div.usage-bar:nth-child(3) > div:nth-child(1) > span:nth-child(1)')))

            page_loaded = True  # if both previous elements are found, exit while loop
        except TimeoutException:  # for some reason, we didn't find the username/password fields
            print("Login timeout exception.  Count=" + str(count))
            if count > 1:  # if we haven't tried more than twice
                resolve_stuck_on_login_page(browser, wait, GCI)  # check if we are still on the login screen and attempt to resolve
                count -= 1  # just try again
            elif count > 0:  # if we have tried twice, restart in headless mode
                count -= 1

                # restart browser instance in non-headless mode
                headless_flag = False
                browser, wait = create_browser_instance(headless_flag)

                # may need to log in again
                if (GCI):
                    login_to_GCI(browser, wait)
                else:
                    login_to_ATT(browser, wait)
            else:  # we have tried 3 times, pause for user to fix issue
                # display error message and wait for user input
                print("Timeout occurred without finding necessary data")
                input("Please fix error and press enter to continue")
                print("Re-navigating to login screen.  Apply necessary changes to script")


def login_to_GCI(browser, wait):
    '''
    Function logs into GCI
    Parameters:
        browser: handle on Firefox browser instance
        wait: object used to have browser handle wait on HTML elements to appear
    '''

    wait_for_login_page(browser, wait, True)  # waiting for elements to load

    # enter username and password and then press login button
    user_elem = browser.find_element_by_id('username')
    user_elem.send_keys("Senlis")
    pass_elem = browser.find_element_by_id('password')
    pass_elem.send_keys(GCI_password)
    login_button = browser.find_element_by_id('login')
    login_button.click()

    print("login complete")


def login_to_ATT(browser, wait):
    '''
    Function navigates to AT&T login screen, enters username and password, and logs in
    Parameters:
        browser: handle on Firefox browser instance
        wait: object used to have browser handle wait on HTML elements to appear
    '''
    wait_for_login_page(browser, wait, False)  # wait for page elements to load

    # enter username and password and then press login button
    user_elem = browser.find_element_by_id('userName')
    user_elem.send_keys("gizmo.romick@gmail.com")
    pass_elem = browser.find_element_by_id('password')
    pass_elem.send_keys(ATT_password)
    login_button = browser.find_element_by_id('loginButton')
    login_button.click()
    # after last command, selenium navigates to "https://m.att.com/my/#/accountOverview"

    print("login complete")


def create_browser_instance(headless_flag):
    # set up the firefox webdriver
    browser_options = Options()

    # this if statement controls whether the browser starts headless (no visible browser window)
    if (headless_flag):
        browser_options.add_argument('-headless')

    # create browser object
    browser = webdriver.Firefox(firefox_options=browser_options)

    # set default wait times
    wait = WebDriverWait(browser, timeout=10)

    return (browser, wait)


def on_login_screen(browser, wait):
    '''
    function checks if browser is currently waiting on login screen
    parameters
       browser: handle on browser object
       wait: handle on wait object
    '''
    GCI_login_URL = "https://login.gci.com/#quick-link"
    ATT_login_URL = "https://www.att.com/my/#/login"
    if browser.current_url == GCI_login_URL or browser.current_url == ATT_login_URL:
        return True

    return True


def resolve_stuck_on_login_page(browser, wait, GCI):
    '''
    function checks if we are still on login page and attempts to resolve issue
    parameters
       browser: handle on browser object
       wait: handle on wait object
       GCI: if true, working on GCI data.  If false, AT&T
    '''
    if on_login_screen(browser, wait):  # we had a problem that prevented the browser from going to the next screen
        print("Error, browser did not proceed to next page after login")
        browser, wait = create_browser_instance(False) # recreate browser instance in non-headless
        if GCI:
            login_to_GCI(browser, wait)
        else:
            login_to_ATT(browser, wait)

        input("Browser restared in headless mode.  Press enter when problem is resolved")


# **************************** setup section **************************
# flags
data_gathered = False  # when we get the data from the page we need, this flag allows us to continue

# variable
count = 3  # used to monitor how many times we try to navigate to a page

browser, wait = create_browser_instance(headless_flag)  # create a browser

# **************************** GCI section **************************
login_to_GCI(browser, wait)  # function will log in for us

print("collecting data")

wait_for_data_page(browser, wait, True)  # function will wait for data elements to appear

# identify data elements
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

# **************************** AT&T section **************************
login_to_ATT(browser, wait)

print("collecting data")

wait_for_data_page(browser, wait, False)

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

# **************************** calculation section **************************
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
