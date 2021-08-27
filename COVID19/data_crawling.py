from selenium import webdriver 
from bs4 import BeautifulSoup 
from datetime import datetime 

driver = webdriver.Chrome('./chromedriver.exe')
url = 'https://www.naver.com'
driver.get(url)

# time.sleep(2)
driver.find_element_by_xpath('//*[@id="query"]').send_keys('코로나 현황')
driver.find_element_by_xpath('//*[@id="search_btn"]').click()

# 국내현황
driver.find_element_by_xpath('//*[@id="_cs_production_type"]/div/div[2]/div/div/ul/li[2]/a/span').click()

# 지역별 표 조회 }
driver.find_element_by_xpath('//*[@id="_cs_production_type"]/div/div[4]/div/div[1]/div/div/div/ul/li[2]/a/span').click()