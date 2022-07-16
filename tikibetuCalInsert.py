from datetime import datetime
import json
from pprint import pprint
from insertGoogleCal import *
import configparser
import sys


def auth_cal_id(envName):
    config = configparser.ConfigParser()
    config.read('setting.ini')
    calId = config.get(envName, 'calId')
    return calId


def selectGamble(envName):
    if envName == "kyotei":
        shubetuStr = "競艇"
        colorId = "1"
    if envName == "keirin":
        shubetuStr = "競輪"
        colorId = "2"
    if envName == "keiba":
        shubetuStr = "競馬"
        colorId = "3"
    if envName == "autorace":
        shubetuStr = "オートレース"
        colorId = "4"
    return shubetuStr, colorId


def jikanToDatetime(jikan, kaisaiDay):
    rawStr = f'{nowYear}{kaisaiDay}'
    if jikan == 'midnight':
        returnStr = 'ミッドナイト'
        rawDateStart = f'{rawStr} 20:00'
        rawDateEnd = f'{rawStr} 23:30'
        startTime = datetime.strptime(rawDateStart, '%Y%m/%d %H:%M')
        endTime = datetime.strptime(rawDateEnd, '%Y%m/%d %H:%M')
    if jikan == 'nighter':
        rawDateStart = f'{rawStr} 15:00'
        rawDateEnd = f'{rawStr} 20:50'
        startTime = datetime.strptime(rawDateStart, '%Y%m/%d %H:%M')
        endTime = datetime.strptime(rawDateEnd, '%Y%m/%d %H:%M')
        returnStr = 'ナイター'
    if jikan == 'morning':
        returnStr = 'モーニング'
        rawDateStart = f'{rawStr} 09:00'
        rawDateEnd = f'{rawStr} 15:00'
        startTime = datetime.strptime(rawDateStart, '%Y%m/%d %H:%M')
        endTime = datetime.strptime(rawDateEnd, '%Y%m/%d %H:%M')
    if jikan == 'summer':
        returnStr = 'サマータイム'
        rawDateStart = f'{rawStr} 12:30'
        rawDateEnd = f'{rawStr} 18:30'
        startTime = datetime.strptime(rawDateStart, '%Y%m/%d %H:%M')
        endTime = datetime.strptime(rawDateEnd, '%Y%m/%d %H:%M')
    return returnStr, startTime, endTime


def judgeKubun(kubun):
    if kubun == "kanto":
        return ['関東', kubun]
    if kubun == "tyuokoti":
        return []
    if kubun == "hokkaido":
        return []
    if kubun == "tohoku":
        return []
    if kubun == "hokuriku":
        return []
    if kubun == "tokai":
        return []
    if kubun == "kinki":
        return []
    if kubun == "tyugoku":
        return []
    if kubun == "sikoku":
        return []
    if kubun == "kyushu":
        return []


envName = sys.argv[1]
kubunName = sys.argv[2]
nowYear = '2022'
calendarId = auth_cal_id("tokai")
shubetuStr, colorId = selectGamble(envName)
colorId = 1

loadJson = json.load(open(f'{envName}.json'))

for i in loadJson.items():
    # if i[0] == '7/14':
    for j in i[1]:
        if j.get('ken') == "近畿":
            classs = ""
            if j.get('class') != None:
                classs = j['class']
            if j.get('class') == None:
                classs = ""
            if j.get('jikan') != None:
                jyo = j['jyo']
                jikan, startTime, endTime = jikanToDatetime(
                    j['jikan'], i[0])
                insStr = f'{jyo}{classs}{jikan}{startTime}{endTime}'
                print(insStr)
                insertGoogleCal(f'{jyo}{shubetuStr}',
                                startTime, endTime, colorId, calendarId)
            else:
                jyo = j['jyo']
                startTime = datetime.strptime(
                    f'{nowYear}{i[0]} 12:00', '%Y%m/%d %H:%M')
                endTime = datetime.strptime(
                    f'{nowYear}{i[0]} 17:00', '%Y%m/%d %H:%M')
                jikan = "日中"
                insStr = f'{jyo}{jikan}{startTime}{endTime}'
                print(insStr)
                insertGoogleCal(f'{jyo}{shubetuStr}',
                                startTime, endTime, colorId, calendarId)
