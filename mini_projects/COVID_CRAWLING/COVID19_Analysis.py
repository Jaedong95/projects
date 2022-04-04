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

import pandas as pd 

columns = ['수집일자', '지역', '누적확진자', '신규확진자']
pd_data = pd.DataFrame(covid_regions, columns = columns)

driver.find_element_by_xpath('//*[@id="_cs_production_type"]/div/div[4]/div/div[1]/div/div/div/ul/li[4]/a/span').click()

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
driver.close()

import pymysql 

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='covid',charset='utf8')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS regions (date char(10), region char(10), covid_total int, covid_today int)')

for i in range(len(covid_regions)):
    total_c = int(covid_regions[i][2].replace(',',''))
    today_c = int(covid_regions[i][3].replace(',',''))
    sql = "INSERT INTO `regions` VALUES(%s, %s, %s, %s)"
    cur.execute(sql, (covid_regions[i][0], covid_regions[i][1], total_c, today_c))

conn.commit()
conn.close()

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='covid',charset='utf8')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS weeks (date char(10), `국내발생` int, `해외유입` int , `신규확진자수` int)')

for i in range(len(covid_week)):
    occur_i = int(covid_week[i][1].replace(',',''))
    occur_o = int(covid_week[i][2].replace(',',''))
    total_c = int(covid_week[i][3].replace(',',''))
    sql = "INSERT INTO `weeks` VALUES(%s, %s, %s, %s)"
    cur.execute(sql, (covid_week[i][0], occur_i, occur_o, total_c))

conn.commit()

covid_regions = [] 

cur.execute('SELECT * FROM regions')
datas = cur.fetchall()

for data in datas:
    covid_regions.append([data[0], data[1], data[2], data[3]])

covid_regions

covid_week = []

cur.execute('SELECT * FROM weeks')
datas = cur.fetchall()

for data in datas:
    covid_week.append([data[0], data[1], data[2], data[3]])
    
conn.close()

region_columns = ['수집일자', '지역', '누적확진자', '신규확진자']
week_columns = ['일자','국내 발생','해외 유입', '신규 합계']

pd_region = pd.DataFrame(covid_regions, columns = region_columns)
pd_week = pd.DataFrame(covid_week, columns = week_columns)

pd_region.head()
pd_region.tail()
pd_region.describe()

sum_new_p = sum(pd_region['신규확진자'])
pd_region['신규 확진자 비율 (%)'] = round(pd_region['신규확진자'] / sum_new_p * 100, 1)
pd_region.head()
pd_region.sort_values(by='신규확진자', ascending=False).head()

pd_week.head()
pd_week.tail()
pd_week.describe()
pd_week.sort_values(by='신규 합계', ascending=False).head()

import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib import font_manager, rc 
import platform

# 그래프에서 한글을 표기하기 위해 글꼴 변경 
if platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font',family=font_name)
elif platform.system() == 'Darwin':   # macOS
    rc('font',family = 'AppleGothic')
else:
    print('Check your OS system')

x = np.array(7)
date_info = []
value_1 = []
value_2 = [] 
value_3 = [] 

for i in range(7):
    date_info.append(pd_week['일자'][i])
    value_1.append(pd_week['국내 발생'][i])
    value_2.append(pd_week['해외 유입'][i])
    value_3.append(pd_week['신규 합계'][i])

p1 = plt.bar(date_info, value_1, color='b', alpha=0.5, width=0.5)
p2 = plt.bar(date_info, value_2, color='r', alpha=0.5,bottom=value_1,width=0.5)
plt.title('최근 7일간 국내발생 및 해외유입 코로나 신규확진자 수',fontsize=15,pad=20)
plt.ylabel('신규확진자 수',fontsize=13)
plt.xlabel('일자',fontsize=13)
plt.xticks(date_info,fontsize=15)
plt.ylim([0,3000])
plt.legend((p1[0],p2[0]), ('국내 발생','해외 유입'), fontsize=15)
plt.show()


# In[ ]:




