import pandas as pd 
asd
def data_analysis(covid_regions, covid_week):
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

    return pd_region, pd_week 

# 데이터 시각화 
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib import font_manager, rc 
import platform

def show_data(pd_week):
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

