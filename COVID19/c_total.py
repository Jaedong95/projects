from selenium import webdriver 
from bs4 import BeautifulSoup 
from datetime import datetime 

driver = webdriver.Chrome('./chromedriver.exe')
url = 'https://www.naver.com'
driver.get(url)

# time.sleep(2)
driver.find_element_by_xpath('//*[@id="query"]').send_keys('코로나 현황')
driver.find_element_by_xpath('//*[@id="search_btn"]').click()