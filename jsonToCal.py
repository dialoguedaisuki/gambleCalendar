from datetime import datetime
import json

# Classキーがない場合を実装する


def jikanToDatetime(jikan, kaisaiDay):
    nowYear = '2022'
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


keirinJson = json.load(open('./autorace.json'))
for i in keirinJson.items():
    if i[0] == '6/13':
        for j in i[1]:
            if j.get('class') != None:
                classs = j['class']
            else:
                classs = ""
            if j.get('jikan') != None:
                jyo = j['jyo']
                jikan, startTime, endTime = jikanToDatetime(j['jikan'], i[0])
                insStr = f'{jyo}{classs}{jikan}{startTime}{endTime}'
                print(insStr)
            else:
                jyo = j['jyo']
                classs = j['class']
                insStr = f'{jyo}{classs}日中'
                startTime = ""
                endTie = ""
                print(insStr)
