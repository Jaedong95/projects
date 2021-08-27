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

# 지역별 표 조회 
driver.find_element_by_xpath('//*[@id="_cs_production_type"]/div/div[4]/div/div[1]/div/div/div/ul/li[2]/a/span').click()

# 테이블 정보 조회 
date_info = str(datetime.today().month).zfill(2) + str(datetime.today().day).zfill(2)
# int(date_info)
covid_regions = [] 

for i in range(1, 4):
    table = driver.find_element_by_xpath('//*[@id="_cs_production_type"]/div/div[4]/div/div[3]/div[{}]/div/table/tbody'.format(i))
    
    for tr_a in table.find_elements_by_tag_name('tr'):
        td = tr_a.find_elements_by_tag_name('td')
        s = "{}, {}, {}\n".format(td[0].text, td[1].text, td[2].text)
        # print(s) 
        covid_regions.append([date_info,td[0].text,td[1].text,td[2].text])
    
    if i != 3:  # 클릭은 두 번만 해야 함 
        driver.find_element_by_xpath('//*[@id="_cs_production_type"]/div/div[4]/div/div[3]/div[5]/div/div/a[2]').click() 

# covid_regions