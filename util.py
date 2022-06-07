from bs4 import BeautifulSoup
from pprint import pprint
import requests
import re
from datetime import datetime, timedelta


def kyoteiGetCal(url):
    soup = urlToBs4(url)
    table = soup.find('div', {'class': "table1"})
    print(table)


def autoRaceGetCal(url):
    pass


def netkeibaGetCal(url):
    soup = urlToBs4(url)
    table = soup.find('table', {'class': "Calendar_Table"})
    calTable = table.find_all("td", class_="RaceCellBox")
    kaisaiCal = []
    for cal in calTable:
        kaisaiDay = cal.find('span', {'class': "Day"}).get_text()
        if kaisaiDay:
            for i in cal.find_all('div', {'class': "kaisai_1"}):
                url = "https://nar.netkeiba.com/top/race_list_sub.html?kaisai_date="
                a_tag = i.find("a")
                href = a_tag.get("href")
                kaisaiBasho = a_tag.find(
                    'span', {'class': "JyoName"}).get_text()
                url += re.findall(
                    "\/top\/race_list.html\?kaisai_date=(.*)$", href)[0]
                if a_tag and href:
                    kaisaiCal.append([kaisaiDay, kaisaiBasho, url])
                    url = ""
    pprint(kaisaiCal)
    return kaisaiCal


def netkeirinSc(url):
    soup = urlToBs4(url)
    mouthSchedule = {}
    table = soup.find('div', {'class': "Race_Calendar_List"})
    calTable = table.find_all("li", {'class': "Calendar_DayList"})
    for cal in calTable:
        keirinLs = []
        kaisaiDay = cal.find(
            'dt', {'class': "ThisWeek_Day"}).get_text().strip()
        kaisaiD = removeYoubi(kaisaiDay)
        kaisaiJyos = cal.find_all("li", {'class': re.compile("^race_grade_*")})
        for jyo in kaisaiJyos:
            dayDict = {}
            # 開催場
            kaisaiJyo = jyo.find(
                'p', {'class': "JyoName"}).get_text().strip()
            dayDict['jyo'] = kaisaiJyo
            # クラス(F)
            kaisaiClass = jyo.find(
                'span', {'class': re.compile("^Icon_GradeType Icon_GradeType*")}).get_text().strip()
            dayDict['classF'] = kaisaiClass
            # ガールズ
            kaisaiGirls = jyo.find(
                'span', {'class': "Icon_RaceMark Girls"})
            if kaisaiGirls != None:
                girls = kaisaiGirls['aria-label']
                dayDict['girls'] = True
            # ミッドナイト
            midnight = jyo.find(
                'span', {'class': "Icon_RaceMark MidNight"})
            if midnight != None:
                midnight = midnight['aria-label']
                dayDict['midnight'] = True
            # ナイター
            nighter = jyo.find(
                'span', {'class': "Icon_RaceMark Nighter"})
            if nighter != None:
                nighter = nighter['aria-label']
                dayDict['nighter'] = True
            # モーニング
            morning = jyo.find(
                'span', {'class': "Icon_RaceMark Morning"})
            if morning != None:
                morning = morning['aria-label']
                dayDict['morning'] = True
            keirinLs.append(dayDict)
        mouthSchedule[kaisaiD] = keirinLs
    pprint(mouthSchedule)
    return mouthSchedule


def removeYoubi(youbi):
    newYoubi = re.sub(r'（.*）', '', youbi)
    return newYoubi


def urlToBs4(url):
    url = url
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    return soup


kyoteiGetCal("https://www.boatrace.jp/owpc/pc/race/index?hd=20220607")

# netkeirinSc(
#     "https://keirin.netkeiba.com/race/race_calendar/?kaisai_year=2022&kaisai_month=6")

# netkeibaGetCal(
#     "https://nar.netkeiba.com/top/calendar.html?year=2022&month=6")