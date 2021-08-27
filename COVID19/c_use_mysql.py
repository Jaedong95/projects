# mysql에 저장하고, 데이터 가져오기 
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

# 지역별 누적 확진자 수 
covid_regions = [] 

cur.execute('SELECT * FROM regions')
datas = cur.fetchall()

for data in datas:
    covid_regions.append([data[0], data[1], data[2], data[3]])

# 최근 7일간 일별 신규 확진자 수 
covid_week = []

cur.execute('SELECT * FROM weeks')
datas = cur.fetchall()

for data in datas:
    covid_week.append([data[0], data[1], data[2], data[3]])
    
conn.close()