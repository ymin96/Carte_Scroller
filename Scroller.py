from Carte import *
from University import *
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import pymysql
import time


class Scroller:

    def __init__(self):
        self.conn = pymysql.connect(host='211.33.245.179', port=3307, user='ymin96', passwd='dlflrh18', db='about_time',
                                    autocommit=True)

    def addUniversity(self, university):
        curs = self.conn.cursor()
        sql = "delete from Carte where title = %s"
        curs.execute(sql, (university.title))
        for carte in university.cartes:
            sql = "insert into Carte(title, day, breakfast, lunch, supper, num) values (%s, %s, %s, %s, %s, %s)"
            curs.execute(sql, (university.title, carte.day, carte.breakfast, carte.lunch, carte.supper, carte.num))

    def kunsan_uni(self):
        print('start kunsan_university')
        try:
            while(True):
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
                break
            self.addUniversity(kunsan)
        except BaseException as e:
            print(e)
            print('retry kunsan_university')
        print('finish kunsan_university')

    def jeonju_uni(self):
        # 크롬 headless 모드 실행
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_argument('headless')
        chrome_option.add_argument('--disable-gpu')
        chrome_option.add_argument('lang=ko_KR')
        chrome_option.add_argument('--window-size=1920,1080')
        print('start jeonju_university')
        try:
            while (True):
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
                jeonju = University("전주대학교")
                for i in range(5):
                    carte = Carte(day[i],breakfast[i],lunch[i],supper[i],num[i])
                    jeonju.addCarte(carte)
                print("finish jeonju_university")
                break
            self.addUniversity(jeonju)
        except:
            print('error: retry jeonju_university')

        def run(self):
            cursor = self.conn.cursor()
            cursor.execute("SELECT VERSION()")
            data = cursor.fetchone()

            print("Database version : %s " % data)
            self.conn.close()
