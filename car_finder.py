from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import os


chromedriver_location = os.path.realpath("chromedriver")
options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# this open up a blank useable automated chrome window
driver = webdriver.Chrome(executable_path=chromedriver_location, chrome_options=options)

driver.get("https://raleigh.craigslist.org/search/cta")


def set_min_price(driver, price):
    elem = driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div/div[4]/input[1]')
    elem.clear()
    elem.send_keys(str(price))
    return

def set_max_price(driver, price):
    elem = driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div/div[4]/input[2]')
    elem.clear()
    elem.send_keys(str(price))
    return

def set_min_year(driver, year):
    elem = driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div/div[6]/div[1]/input[1]')
    elem.clear()
    elem.send_keys(str(year))
    return

def set_max_year(driver, year):
    elem = driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div/div[6]/div[1]/input[2]')
    elem.clear()
    elem.send_keys(str(year))
    return

def set_search(driver, search_parameter):
    elem = driver.find_element_by_xpath('//*[@id="query"]')
    elem.clear()
    elem.send_keys(str(search_parameter))
    return

def start_search(driver):
    elem = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchform"]/div[1]/button/span[1]')))
    elem.click()
    return

set_min_price(driver, 1000)
set_max_price(driver, 20000)
set_min_year(driver, 1990)
set_max_year(driver, 2000)
set_search(driver, "Nissan GTR")
start_search(driver)







# sleep(1)
# elem = driver.find_element_by_id('searchBox')
#
# elem.clear()
# elem.send_keys('CAT00058')
# sleep(1)
# elem.send_keys(Keys.RETURN)
#
# try:
#     # Find the first result of the search box and click it
#     sleep(.5)
#     elem = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="navContainerCollapse"]/div/ul/li[2]/a/div[1]')))
#     sleep(1)
#     elem.click()
# except:
#     print "Failed Start up"
#     pass
#
# WebDriverWait(driver, 240).until(EC.invisibility_of_element_located((By.ID, 'noSearch')))
# sleep(.5)
