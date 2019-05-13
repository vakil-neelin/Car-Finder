from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep

chromedriver_location = r'chromedriver.exe'
options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# this open up a blank useable automated chrome window
driver = webdriver.Chrome(chromedriver_location, chrome_options=options)

driver.get("https://raleigh.craigslist.org/search/cta")



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
