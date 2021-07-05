import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from os import path

def get_suburb_data(search_term,search_status):


    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver=webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    #options = Options()
    #options.headless = False
    #options.add_argument('--disable-blink-features=AutomationControlled')
    #driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    #driver.implicitly_wait(10)
    #driver.maximize_window()

    search_term_data = pd.DataFrame(columns = ['PRICE','ADDRESS','BEDS','BATHS','CARS','SIZE','TYPE','SALE_DATE'])

    if search_status == 'Sold':
        driver.get('https://www.realestate.com.au/sold')
    elif search_status == 'For Sale':
        driver.get('https://www.realestate.com.au/buy')
    elif search_status == 'For Rent':
        driver.get('https://www.realestate.com.au/rent')

    try:
        el = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "rui-search-button")))
        print("Search page is ready!")

    except TimeoutException:
        print("Loading search page took too much time!")

    search = driver.find_element_by_xpath("//input").send_keys(search_term)
    surrounding = driver.find_element_by_class_name("formSuburbSurroundings").click()
    submit = driver.find_element_by_class_name("rui-search-button").click()

    while(True):
        try:
            el = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='residential-card__content']")))
            print("Next page is ready!")
        except TimeoutException:
            print("Loading next page took too much time!")

        card_content = driver.find_elements_by_xpath("//div[@class='residential-card__content']")
        for card in card_content:
            row_data = []
            try:
                row_data.insert(0,card.find_element_by_class_name("property-price ").text)
            except NoSuchElementException:
                row_data.insert(0,'null')
            try:
                row_data.insert(1,card.find_element_by_class_name("residential-card__address-heading").text)
            except NoSuchElementException:
                row_data.insert(1, 'null')
            try:
                row_data.insert(2,card.find_element_by_class_name("piped-content").find_element_by_xpath(".//span[@class='general-features__icon general-features__beds']").text)
            except NoSuchElementException:
                row_data.insert(2, 'null')
            try:
                row_data.insert(3,card.find_element_by_class_name("piped-content").find_element_by_xpath(".//span[@class='general-features__icon general-features__baths']").text)
            except NoSuchElementException:
                row_data.insert(3, 'null')
            try:
                row_data.insert(4,card.find_element_by_class_name("piped-content").find_element_by_xpath(".//span[@class='general-features__icon general-features__cars']").text)
            except NoSuchElementException:
                row_data.insert(4, 'null')
            try:
                row_data.insert(5,card.find_element_by_class_name("piped-content").find_element_by_xpath(".//span[@class='property-size__icon property-size__land']").text)
            except NoSuchElementException:
                row_data.insert(5, 'null')
            try:
                row_data.insert(6,card.find_element_by_class_name("piped-content").find_element_by_xpath(".//span[@class='residential-card__property-type']").text)
            except NoSuchElementException:
                row_data.insert(6, 'null')
            try:
                row_data.insert(7,(card.find_element_by_xpath("./span").text).replace("Sold on ",""))
            except NoSuchElementException:
                row_data.insert(7, 'null')

            print(row_data)
            search_term_data.loc[len(search_term_data)] = row_data

        try:
            next_page = driver.find_element_by_class_name("results-set-footer").find_element_by_xpath(".//a[@class='rui-button-brand pagination__link-next']").click()
            time.sleep(5)
        except NoSuchElementException:
            return search_term_data

    return search_term_data