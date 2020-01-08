from Carte import *
from University import *
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from types import *
from sqlalchemy import pool
import pymysql
import time
import threading


class Scroller:

    def __init__(self, id, pw):
        try:
            self.mypool = pool.QueuePool(
                lambda: pymysql.connect(host='211.33.245.179', port=3307, user=id, passwd=pw, db='about_time',
                                    autocommit=True), pool_size=5, max_overflow=0)
        except:
            print("DB connected failed")
            exit(-1)

    # db insert university
    def addUniversity(self, university, conn):
        curs = conn.cursor()
        sql = "delete from Carte where title = %s"
        curs.execute(sql, (university.title))
        for carte in university.cartes:
            sql = "insert into Carte(title, day, breakfast, lunch, supper, num) values (%s, %s, %s, %s, %s, %s)"
            curs.execute(sql, (university.title, carte.day, carte.breakfast, carte.lunch, carte.supper, carte.num))

    # 군산대학교
    def setkunsan_uni(self):

        conn = self.mypool.connect()
        print('start kunsan_university')
        for k in range(10):
            try:
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
                    breakfast.append(i.get_text().strip().replace(' ', '<br>'))
                for i in lunch_t.find_all('td'):
                    lunch.append(i.get_text().strip().replace(' ', '<br>'))
                for i in supper_t.find_all('td'):
                    supper.append(i.get_text().strip().replace(' ', '<br>'))

                kunsan = University('군산대학교')
                for i in range(7):
                    carte = Carte(day[i], breakfast[i], lunch[i], supper[i], i)
                    kunsan.addCarte(carte)
                self.addUniversity(kunsan, conn)
                conn.close()
                break
            except BaseException as e:
                print("error: " + e)
                print('retry kunsan_university('+str(k)+')')
                time.sleep(1)
        print('finish kunsan_university')

    # 전주대학교
    def setJeonju_uni(self):
        conn = self.mypool.connect()
        # 크롬 headless 모드 실행
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_argument('headless')
        chrome_option.add_argument('--disable-gpu')
        chrome_option.add_argument('lang=ko_KR')
        chrome_option.add_argument('--window-size=1920,1080')
        print('start jeonju_university')
        for k in range(10):
            try:
                driver = webdriver.Chrome("driver/chromedriver", chrome_options=chrome_option)
                driver.get("https://startower.jj.ac.kr/")
                time.sleep(1)
                driver.find_element_by_id("mainframe_childframe_form_DivMenuFrame_DivMainMenu_btn_MainMenu03").click()
                time.sleep(0.5)
                driver.find_element_by_id("mainframe_childframe_form_DivMenuFrame_DivSubMenu_btn_SubMenu04").click()
                time.sleep(0.5)
                breakfast = []
                lunch = []
                supper = []
                day = []
                num = []
                for i in range(1, 6):
                    driver.find_element_by_id("mainframe_childframe_form_DivMain_btn_Preview0" + str(i)).click()
                    day.append(
                        driver.find_element_by_id("mainframe_childframe_form_DivMain_btn_Preview0" + str(i)).text)
                    driver.switch_to_frame('mainframe_childframe_form_DivMain_web_Content_WebBrowser')
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    breakfast.append(
                        soup.find_all('tr')[0].find_all('td')[1].get_text().strip().replace('\t\t\t\t', '<br>'))
                    lunch.append(
                        soup.find_all('tr')[2].find_all('td')[1].get_text().strip().replace('\t\t\t\t', '<br>'))
                    supper.append(
                        soup.find_all('tr')[3].find_all('td')[1].get_text().strip().replace('\t\t\t\t', '<br>'))
                    num.append(i)
                    driver.switch_to_default_content()
                driver.close()
                jeonju = University("전주대학교")
                for i in range(5):
                    carte = Carte(day[i], breakfast[i], lunch[i], supper[i], num[i])
                    jeonju.addCarte(carte)
                print("finish jeonju_university")
                self.addUniversity(jeonju, conn)
                conn.close()
                break
            except BaseException as e:
                print(e)
                print('retry jeonju_university('+str(k)+')')
                time.sleep(1)

    # 전북대학교(직영관)
    def setJeonbuk_uni1(self):
        conn = self.mypool.connect()
        print("start: jeonbuk_university1")
        for k in range(10):
            try:
                url = "https://likehome.jbnu.ac.kr/home/main/inner.php?sMenu=B7100"
                page = urlopen(url)
                soup = BeautifulSoup(page, "html.parser")

                table = soup.find('table')
                thead = table.find('thead')
                tbody = table.find('tbody')

                day = []
                breakfast = []
                lunch = []
                supper = []
                num = []

                for i in thead.find_all('th'):
                    day.append(i.get_text().strip().replace(" ", "").replace("\t\t", ""))
                del day[0]

                for i in range(7):
                    breakfast.append(
                        tbody.find_all('tr')[0].find_all('td')[i].get_text().replace("\n", "").replace(" ", "<br>"))
                    lunch.append(
                        tbody.find_all('tr')[1].find_all('td')[i].get_text().replace("\n", "").replace(" ", "<br>"))
                    supper.append(
                        tbody.find_all('tr')[2].find_all('td')[i].get_text().replace("\n", "").replace(" ", "<br>"))
                    num.append(i)

                jeonbuk = University("전북대학교(직영관)")
                for i in range(7):
                    carte = Carte(day[i], breakfast[i], lunch[i], supper[i], num[i])
                    jeonbuk.addCarte(carte)
                self.addUniversity(jeonbuk, conn)
                conn.close()
                break
            except BaseException as e:
                print(e)
                print("retry: jeonbuk_university1("+str(k)+')')
                time.sleep(1)
        print("finish: jeonbuk_university1")

    # 전북대학교(참빛관)
    def setJeonbuk_uni2(self):
        conn = self.mypool.connect()
        print("start: jeonbuk_university2")
        for k in range(10):
            try:
                url = "https://likehome.jbnu.ac.kr/home/main/inner.php?sMenu=B7200"
                page = urlopen(url)
                soup = BeautifulSoup(page, "html.parser")

                table = soup.find('table')
                thead = table.find('thead')
                tbody = table.find('tbody')

                day = []
                breakfast = []
                lunch = []
                supper = []
                num = []

                for i in thead.find_all('th'):
                    day.append(i.get_text().strip().replace(" ", "").replace("\t\t", ""))
                del day[0]

                for i in range(7):
                    breakfast.append(
                        tbody.find_all('tr')[0].find_all('td')[i].get_text().replace("\n", "").replace(" ", "<br>"))
                    lunch.append(
                        tbody.find_all('tr')[1].find_all('td')[i].get_text().replace("\n", "").replace(" ", "<br>"))
                    supper.append(
                        tbody.find_all('tr')[2].find_all('td')[i].get_text().replace("\n", "").replace(" ", "<br>"))
                    num.append(i)

                jeonbuk = University("전북대학교(참빛관)")
                for i in range(7):
                    carte = Carte(day[i], breakfast[i], lunch[i], supper[i], num[i])
                    jeonbuk.addCarte(carte)
                self.addUniversity(jeonbuk, conn)
                conn.close()
                break
            except BaseException as e:
                print(e)
                print("retry: jeonbuk_university2("+str(k)+')')
                time.sleep(1)
        print("finish: jeonbuk_university2")

    # 전북대학교(특성화캠퍼스)
    def setJeonbuk_uni3(self):
        conn = self.mypool.connect()
        print("start: jeonbuk_university3")
        for k in range(10):
            try:
                url = "https://likehome.jbnu.ac.kr/home/main/inner.php?sMenu=B7300"
                page = urlopen(url)
                soup = BeautifulSoup(page, "html.parser")

                table = soup.find('table')
                thead = table.find('thead')
                tbody = table.find('tbody')

                day = []
                breakfast = []
                lunch = []
                supper = []
                num = []

                for i in thead.find_all('th'):
                    day.append(i.get_text().strip().replace(" ", "").replace("\t\t", ""))
                del day[0]

                for i in range(7):
                    if tbody.find_all('tr')[0].find_all('td')[i].find('a') is not None:
                        breakfast.append(tbody.find_all('tr')[0].find_all('td')[i].find('a')['title'].replace(',', '<br>'))
                    else:
                        breakfast.append("")
                    if tbody.find_all('tr')[1].find_all('td')[i].find('a') is not None:
                        lunch.append(tbody.find_all('tr')[1].find_all('td')[i].find('a')['title'].replace(',', '<br>'))
                    else:
                        lunch.append("")
                    if tbody.find_all('tr')[2].find_all('td')[i].find('a') is not None:
                        supper.append(tbody.find_all('tr')[2].find_all('td')[i].find('a')['title'].replace(',', '<br>'))
                    else:
                        supper.append("")
                    num.append(i)

                jeonbuk = University("전북대학교(특성화캠퍼스)")
                for i in range(7):
                    carte = Carte(day[i], breakfast[i], lunch[i], supper[i], num[i])
                    jeonbuk.addCarte(carte)
                self.addUniversity(jeonbuk, conn)
                conn.close()
                break
            except BaseException as e:
                print(e)
                print("retry: jeonbuk_university3("+str(k)+')')
                time.sleep(1)
        print("finish: jeonbuk_university3")

    # 원광대학교
    def setWonkwang_uni(self):
        conn = self.mypool.connect()
        # 크롬 headless 모드 실행
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_argument('headless')
        chrome_option.add_argument('--disable-gpu')
        chrome_option.add_argument('lang=ko_KR')
        chrome_option.add_argument('--window-size=1920,1080')

        print('start: wonkwang_university')
        for k in range(10):
            try:
                driver = webdriver.Chrome("driver/chromedriver", chrome_options=chrome_option)
                driver.get("https://dorm.wku.ac.kr/?cat=6")
                driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[0].find_element_by_tag_name(
                    'a').click()

                html = driver.page_source
                driver.close()
                soup = BeautifulSoup(html, "html.parser")
                table = soup.find('table', 'tbl_type').find('tbody')

                temp = [["" for j in range(7)] for i in range(3)]
                day = []
                num = [i for i in range(7)]

                for i in table.find('tr').find_all('th'):
                    day.append(i.get_text())
                del day[0]

                for i in range(3):
                    for j in range(7):
                        temp[i][j] += table.find_all('tr')[(i * 5) + 1].find_all('td')[j + 2].get_text().replace('\xa0',
                                                                                                                 '') + '<br>'
                        temp[i][j] += table.find_all('tr')[(i * 5) + 2].find_all('td')[j + 1].get_text() + '<br>'
                        temp[i][j] += table.find_all('tr')[(i * 5) + 3].find_all('td')[j + 1].get_text() + '<br>'
                        temp[i][j] += table.find_all('tr')[(i * 5) + 4].find_all('td')[j].get_text() + '<br>'
                        temp[i][j] += table.find_all('tr')[(i * 5) + 5].find_all('td')[j].get_text().strip().replace(
                            '\n/', '<br>').replace('\n', '<br>')
                breakfast = temp[0]
                lunch = temp[1]
                supper = temp[2]

                wonkwang = University('원광대학교')
                for i in range(7):
                    carte = Carte(day[i], breakfast[i], lunch[i], supper[i], num[i])
                    wonkwang.addCarte(carte)
                self.addUniversity(wonkwang, conn)
                conn.close()
                break
            except BaseException as e:
                print(e)
                print('retry: wonkwang_university('+str(k)+')')
                time.sleep(1)
        print('finish wonkwang_university')

    def run(self):
        result = []

        # Scroller 클래스에서 set으로 시작하는 메소드만 추출
        for attr, val in Scroller.__dict__.items():
            if type(val) == FunctionType and attr[:3] == 'set':
                result.append(attr)

        # 위에서 추출한 메소드를 스레드로 실행
        for func in result:
            running = getattr(self, func)
            thread = threading.Thread(target=running)
            thread.start()
