from bs4 import BeautifulSoup
from pprint import pprint
import requests
import re
from datetime import datetime, timedelta, date


def autoRaceGetCal(url):
    soup = urlToBs4(url)
    baseTable = soup.find('table', {'class': "tb70 w100pr"})
    loopTable = [i for i in baseTable.find_all("tr")]
    dayLs = []
    for i in loopTable:
        dayDict = {}
        jyoInfo = i.find('th', {'class': 'course'})
        if jyoInfo != None:
            jyo = jyoInfo.get_text(',').split(',')[0]
            dayDict['jyo'] = jyo
            try:
                soutaiKaisaiDay = jyoInfo.get_text(',').split(',')[1]
                dayDict['kaisaiDay'] = soutaiKaisaiDay
            except Exception as e:
                print(e)
        raceName = i.find('ul', {'class': 'raceName'})
        raceNameRawHtml = raceName.find("li")
        mainRace = raceNameRawHtml.get_text().strip()
        dayDict['mainRace'] = mainRace
        raceNameLs = raceNameRawHtml.find_all('img')
        for j in raceNameLs:
            if j['alt'] in "G":
                dayDict['class'] = j['alt']
            if j['alt'] in "モーニング":
                dayDict['morning'] = True
            if j['alt'] in "ナイター":
                dayDict['nighter'] = True
            if j['alt'] in "ミッドナイト":
                dayDict['midnight'] = True
        dayLs.append(dayDict)
    return dayLs


def MouthUrlParser(url, defdef):
    baseUrl = url
    d1 = date(2022, 6, 10)
    d2 = date(2022, 6, 11)
    dictLs = {}
    for i in range((d2 - d1).days + 1):
        execDay = d1 + timedelta(i)
        execDayStr = execDay.strftime("%Y%m%d")
        m = execDay.strftime("%m").lstrip('0')
        d = execDay.strftime("%d").lstrip('0')
        keyDay = f'{m}/{d}'
        url = f'{baseUrl}{execDayStr}'
        dayLs = defdef(url)
        dictLs[keyDay] = dayLs
    pprint(dictLs)
    return dictLs


def kyoteiGetCal(url):
    soup = urlToBs4(url)
    table = soup.find('div', {'class': "table1"})
    rows = table.find_all("tbody")
    dayLs = []
    for i in rows:
        dayDict = {}
        # 開催場所
        jyo = i.find("img")['alt']
        dayDict['jyo'] = jyo
        # 開催種別
        nighter = i.find('td', {'class': 'is-nighter'})
        if nighter != None:
            dayDict['nighter'] = True
        summer = i.find('td', {'class': 'is-summer'})
        if summer != None:
            dayDict['summer'] = True
        morning = i.find('td', {'class': 'is-morning'})
        if morning != None:
            dayDict['morning'] = True
        # 一般
        ippan = i.find('td', {'class': 'is-ippan'})
        if ippan != None:
            dayDict['Class'] = "ippan"
        # SG
        sg = i.find('td', {'class': "is-SGa"})
        if sg != None:
            dayDict["Class"] = "SG"
        # G1
        g1 = i.find('td', {'class': "is-G1b"})
        if g1 != None:
            dayDict["Class"] = "G1"
        # G2
        g2 = i.find('td', {'class': "is-G2b"})
        if g2 != None:
            dayDict["Class"] = "G2"
        # G3
        g3 = i.find('td', {'class': "is-G3b"})
        if g3 != None:
            dayDict["Class"] = "G3"
        # レディース
        lady = i.find('td', {'class': re.compile(".*is-lady")})
        if lady != None:
            dayDict['lady'] = True
        dayLs.append(dayDict)
    return dayLs


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
            dayDict['class'] = kaisaiClass
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


netkeirinSc(
    "https://keirin.netkeiba.com/race/race_calendar/?kaisai_year=2022&kaisai_month=6")
autoRaceBaseurl = "https://www.oddspark.com/autorace/KaisaiRaceList.do?raceDy="
MouthUrlParser(autoRaceBaseurl, autoRaceGetCal)
kyoteiBaseUrl = "https://www.boatrace.jp/owpc/pc/race/index?hd="
MouthUrlParser(kyoteiBaseUrl, kyoteiGetCal)

# netkeibaGetCal(
#     "https://nar.netkeiba.com/top/calendar.html?year=2022&month=6")
