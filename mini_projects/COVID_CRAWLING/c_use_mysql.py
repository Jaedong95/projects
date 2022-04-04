''' mysql Database에 데이터 저장 및 가져오기 '''
import pymysql 

def connect_db():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='covid',charset='utf8')
    cur = conn.cursor()
    return conn, cur 

def store_data(conn, cur, cr_data, cw_data):
    cur.execute('CREATE TABLE IF NOT EXISTS regions (date char(10), region char(10), covid_total int, covid_today int)')

    for i in range(len(cr_data)):
        total_c = int(cr_data[i][2].replace(',',''))
        today_c = int(cr_data[i][3].replace(',',''))
        sql = "INSERT INTO `regions` VALUES(%s, %s, %s, %s)"
        cur.execute(sql, (cr_data[i][0], cr_data[i][1], total_c, today_c))

    conn.commit()
    conn.close()
    conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='covid',charset='utf8')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS weeks (date char(10), `국내발생` int, `해외유입` int , `신규확진자수` int)')
    for i in range(len(cw_data)):
        occur_i = int(cw_data[i][1].replace(',',''))
        occur_o = int(cw_data[i][2].replace(',',''))
        total_c = int(cw_data[i][3].replace(',',''))
        sql = "INSERT INTO `weeks` VALUES(%s, %s, %s, %s)"
        cur.execute(sql, (cw_data[i][0], occur_i, occur_o, total_c))
    conn.commit()

def get_data(conn, cur):
# 지역별 누적 확진자 수 
    cr_data = [] 
    cur.execute('SELECT * FROM regions')
    datas = cur.fetchall()

    for data in datas:
        cr_data.append([data[0], data[1], data[2], data[3]])

    # 최근 7일간 일별 신규 확진자 수 
    cw_data = []

    cur.execute('SELECT * FROM weeks')
    datas = cur.fetchall()

    for data in datas:
        cw_data.append([data[0], data[1], data[2], data[3]])
        
    conn.close()