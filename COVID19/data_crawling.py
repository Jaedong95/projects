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

import pandas as pd 

columns = ['수집일자', '지역', '누적확진자', '신규확진자']
pd_data = pd.DataFrame(covid_regions, columns = columns)

# 최근 7일간 일별 코로나 신규 확진자 데이터 수집 
driver.find_element_by_xpath('//*[@id="_cs_production_type"]/div\
        /div[4]/div/div[1]/div/div/div/ul/li[4]/a/span').click()

# 일주일 동안의 Covid 정보 저장 
covid_week = []

for i in range(1,8):
    driver.find_element_by_xpath('//*[@id="target2"]/dl/div[{}]/dd[1]'.format(i)).click()
    date_info = driver.find_element_by_xpath('//*[@id="_cs_production_type"]/div/div[4]/div/div[5]/div[1]/div[1]/div/div[1]/dl/div[1]/dd[1]').text
    occur_i = driver.find_element_by_xpath('//*[@id="_cs_production_type"]/div/div[4]/div/div[5]/div[1]/div[1]/div/div[1]/dl/div[2]/dd[1]').text
    occur_o = driver.find_element_by_xpath('//*[@id="_cs_production_type"]/div/div[4]/div/div[5]/div[1]/div[1]/div/div[1]/dl/div[2]/dd[2]').text
    occur_sum = driver.find_element_by_xpath('//*[@id="_cs_production_type"]/div/div[4]/div/div[5]/div[1]/div[1]/div/div[1]/dl/div[1]/dd[2]').text
    
    covid_week.append([date_info, occur_i, occur_o, occur_sum])

columns = ['일자','국내 발생','해외 유입', '신규 합계']
pd_data = pd.DataFrame(covid_week, columns=columns)
# pd_data.to_excel('./covid_week.xlsx',index=False)   # MySQL로 구현 필요 