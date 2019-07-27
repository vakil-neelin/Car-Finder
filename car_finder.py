from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
import ConfigParser
import requests
import datetime
from report_generator import Report_Generator

class CarFinder:

    def __init__(self):
        # Reads in the list of vehicles
        self.car_list = self.read_in_config()

        # Creates the report
        self.report = Report_Generator()

        return

    # -------------------------------------------------------
    # Function Name: read_in_config
    # Description: Reads in the config file and parses the fields into a list
    # -------------------------------------------------------
    @staticmethod
    def read_in_config():
        list_of_vehicles = []
        config = ConfigParser.ConfigParser()
        config.read('car_parameters.ini')

        for section in config.sections():
            parameter_list = [section]
            parameter_dict = {}

            # Adds the Search
            try:
                search = config.get(section, 'Search')
                parameter_dict['Search'] = str(search)
            except:
                parameter_dict['Search'] = ''

            # Adds the Beginning Year
            try:
                begining_year = config.get(section, 'BeginningYear')
                parameter_dict['BeginningYear'] = str(begining_year)
            except:
                parameter_dict['BeginningYear'] = ''

            # Adds the Ending Year
            try:
                ending_year = config.get(section, 'EndingYear')
                parameter_dict['EndingYear'] = str(ending_year)
            except:
                parameter_dict['EndingYear'] = ''

            # Adds the Start Price
            try:
                start_price = config.get(section, 'StartPrice')
                parameter_dict['StartPrice'] = str(start_price)
            except:
                parameter_dict['StartPrice'] = ''

            # Adds the End Price
            try:
                end_price = config.get(section, 'EndPrice')
                parameter_dict['EndPrice'] = str(end_price)
            except:
                parameter_dict['EndPrice'] = ''

            # Adds the dictionary to the list with the section name
            parameter_list.append(parameter_dict)
            # Adds the parameter list to the overall list of vehicles
            list_of_vehicles.append(parameter_list)

        return list_of_vehicles

    @staticmethod
    def start_chrome_driver():

        # Loads the chromedriver from the local directory
        chromedriver_location = os.path.realpath("chromedriver")
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')

        # this open up a blank useable automated chrome window
        driver = webdriver.Chrome(executable_path=chromedriver_location, chrome_options=options)
        # Goes to the Local Craiglist vehicle page
        driver.get("https://raleigh.craigslist.org/search/cta")

        return driver

    #-------------------------------------------------------
    # Function Name: set_min_price
    # Description: Sets the minimum price for the vehicle
    #-------------------------------------------------------
    @staticmethod
    def set_min_price(driver, price):
        elem = driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div/div[4]/input[1]')
        elem.clear()
        elem.send_keys(str(price))
        return

    # -------------------------------------------------------
    # Function Name: set_max_price
    # Description: Sets the maximum price for the vehicle
    # -------------------------------------------------------
    @staticmethod
    def set_max_price(driver, price):
        elem = driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div/div[4]/input[2]')
        elem.clear()
        elem.send_keys(str(price))
        return

    # -------------------------------------------------------
    # Function Name: set_min_year
    # Description: Sets the minimum year for the vehicle
    # -------------------------------------------------------
    @staticmethod
    def set_min_year(driver, year):
        elem = driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div/div[6]/div[1]/input[1]')
        elem.clear()
        elem.send_keys(str(year))
        return

    # -------------------------------------------------------
    # Function Name: set_max_year
    # Description: Sets the maximum year for the vehicle
    # -------------------------------------------------------
    @staticmethod
    def set_max_year(driver, year):
        elem = driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div/div[6]/div[1]/input[2]')
        elem.clear()
        elem.send_keys(str(year))
        return

    # -------------------------------------------------------
    # Function Name: set_search
    # Description: Inputs the search parameter
    # -------------------------------------------------------
    @staticmethod
    def set_search(driver, search_parameter):
        elem = driver.find_element_by_xpath('//*[@id="query"]')
        elem.clear()
        elem.send_keys(str(search_parameter))
        return

    # -------------------------------------------------------
    # Function Name: start_search
    # Description: Clicks the search button to make the search
    # -------------------------------------------------------
    @staticmethod
    def start_search(driver):
        elem = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchform"]/div[1]/button/span[1]')))
        elem.click()
        return

    # -------------------------------------------------------
    # Function Name: search_for_vehicle
    # Description:
    # -------------------------------------------------------
    def search_for_vehicle(self, driver, input_list):

        min_year = input_list[1]['BeginningYear']
        max_year = input_list[1]['EndingYear']
        min_price = input_list[1]['StartPrice']
        max_price = input_list[1]['EndPrice']
        search_param = input_list[1]['Search']

        self.set_min_year(driver, min_year)
        self.set_max_year(driver, max_year)
        self.set_min_price(driver, min_price)
        self.set_max_price(driver, max_price)
        self.set_search(driver, search_param)
        self.start_search(driver)

        return

    # -------------------------------------------------------
    # Function Name: search_all_vehicles
    # Description: Starts a new browser for each vehicle to search
    # -------------------------------------------------------
    def search_all_vehicles(self):
        for vehicle in self.car_list:
            chrome_driver = self.start_chrome_driver()
            self.search_for_vehicle(chrome_driver, vehicle)
            self.find_results(chrome_driver)
            sleep(5)
        return

    def get_image_summary(self, link, car_name):

        summary = ""

        # Loads the chromedriver from the local directory
        chromedriver_location = os.path.realpath("chromedriver")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        # this open up a blank useable automated chrome window
        driver = webdriver.Chrome(executable_path=chromedriver_location, chrome_options=options)
        # Goes to the Local Craiglist vehicle page
        driver.get(str(link))

        img_path = driver.find_element(By.CLASS_NAME, 'gallery').find_element(By.CLASS_NAME, 'swipe').find_element(By.CLASS_NAME, 'swipe-wrap').find_element(By.TAG_NAME, 'img').get_attribute('src')

        # download the url contents in binary format
        r = requests.get(img_path)
        # open method to open a file on your system and write the contents
        with open("Images/" + str(car_name) + ".png", "wb") as code:
            code.write(r.content)

        summary = driver.find_element(By.ID, 'postingbody').text

        print summary
        driver.close()

        return summary

    def find_results(self, driver):
        results_table = driver.find_element(By.XPATH, '//*[@id="sortable-results"]/ul')
        # time.sleep(10)

        results = results_table.find_elements(By.TAG_NAME, "li")
        print "Number of Results"
        print len(results)

        for cars in results:
            car_name = cars.find_element(By.CLASS_NAME, "result-info").find_element_by_tag_name('a').text
            car_price = cars.find_element(By.CLASS_NAME, "result-info").find_element(By.CLASS_NAME, "result-meta").find_element(By.CLASS_NAME, "result-price").text
            specific_car_link = cars.find_element(By.TAG_NAME, "a").get_attribute("href")
            summary = self.get_image_summary(specific_car_link, car_name)

            self.report.add_table(car_name, car_price, summary)

        self.report.make_report()

        return

c = CarFinder()
c.search_all_vehicles()

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
