import pymysql 

conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='covid',charset='utf8')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS regions (date char(10), region char(10), covid_total int, covid_today int)')

for i in range(len(covid_regions)):
    total_c = int(covid_regions[i][2].replace(',',''))
    today_c = int(covid_regions[i][3].replace(',',''))
    sql = "INSERT INTO `regions` VALUES(%s, %s, %s, %s)"
    cur.execute(sql, (covid_regions[i][0], covid_regions[i][1], total_c, today_c))
