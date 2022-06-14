from datetime import datetime
import json
from pprint import pprint
from insertGoogleCal import *

nowYear = '2022'


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


keirinJson = json.load(open('./keiba.json'))
shubetuStr = "競馬"
colorId = "4"
for i in keirinJson.items():
    if i[0] == '6/15':
        for j in i[1]:
            classs = ""
            if j.get('class') != None:
                classs = j['class']
            if j.get('class') == None:
                classs = ""
            if j.get('jikan') != None:
                jyo = j['jyo']
                jikan, startTime, endTime = jikanToDatetime(j['jikan'], i[0])
                insStr = f'{jyo}{classs}{jikan}{startTime}{endTime}'
                print(insStr)
                insertGoogleCal(f'{jyo}{shubetuStr}',
                                startTime, endTime, colorId)
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
                                startTime, endTime, colorId)
