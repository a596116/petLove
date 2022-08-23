import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import json
import re


from time import sleep
def qr(name,num):
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values': {'images': 2}}
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--disable-gpu')
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")  
    driver = webdriver.Chrome( options=options)
    driver.get("https://www.qr2copy.com/index.php")

    element = driver.find_element_by_class_name('form-control')
    element.send_keys('https://lovepet.herokuapp.com/view?id='+str(num))
    driver.find_element_by_id('button-addon5').click()
    img = driver.find_element_by_xpath('//*[@id="mainContent"]/div/div/div/div[2]').find_element_by_tag_name('img').get_attribute('src')

    driver.close()
    return img