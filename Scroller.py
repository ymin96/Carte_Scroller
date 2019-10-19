from Carte import *
from University import *
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pymysql


class Scroller:

    def __init__(self):
        self.db = pymysql.connect(host='211.33.245.179', port=3307, user='ymin96', passwd='dlflrh18', db='about_time',
                                  autocommit=True)

    def kunsan_uni(self):
        url = "http://www.kunsan.ac.kr/dormi/index.kunsan?menuCd=DOM_000000704006000000"
        page = urlopen(url)
        soup = BeautifulSoup(page, "html.parser")

        ctable = soup.find_all('table', 'ctable01')[1]
        thead = ctable.find('thead')
        day = thead.find_all('th')
        del (day[0])
        for i in range(0, len(day)):
            temp = day[i].get_text().split('\n')
            day[i] = temp[1] + ',' + temp[2]

        tbody = ctable.find('tbody')

        breakfast_t = tbody.find_all('tr')[0]
        lunch_t = tbody.find_all('tr')[1]
        supper_t = tbody.find_all('tr')[2]

        breakfast = []
        lunch = []
        supper = []
        for i in breakfast_t.find_all('td'):
            breakfast.append(i.get_text().strip().replace(' ', ','))
        for i in lunch_t.find_all('td'):
            lunch.append(i.get_text().strip().replace(' ', ','))
        for i in supper_t.find_all('td'):
            supper.append(i.get_text().strip().replace(' ', ','))

        kunsan = University('군산대학교')
        for i in range(7):
            carte = Carte(day[i], breakfast[i], lunch[i], supper[i])
            kunsan.addCarte(carte)

        print(kunsan)

    def run(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()

        print("Database version : %s " % data)
        self.db.close()
