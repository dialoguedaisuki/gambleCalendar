import json


def jikanToDatetime(jikan):
    if jikan == 'midnight':
        returnStr = 'ミッドナイト'
    if jikan == 'nighter':
        returnStr = 'ナイター'
    if jikan == 'morning':
        returnStr = 'モーニング'
    return returnStr


keirinJson = json.load(open('./kyotei.json'))
for i in keirinJson.items():
    if i[0] == '6/11':
        for j in i[1]:
            if j.get('jikan'):
                jyo = j['jyo']
                classs = j['class']
                jikan = jikanToDatetime(j.get('jikan'))
                insStr = f'{jyo}{classs}{jikan}'
                print(insStr)
            else:
                jyo = j['jyo']
                classs = j['class']
                insStr = f'{jyo}{classs}'
                print(insStr)
