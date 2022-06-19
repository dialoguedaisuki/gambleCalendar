import json
from pprint import pprint

hokkaido = ['北海道']
tohoku = ['青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県']
kanto = ['茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県']
hokuriku = ['富山県', '石川県', '福井県', '新潟県']
tyuoKoti = ['山梨県', '長野県', '岐阜県']
tokai = ['静岡県', '愛知県', '岐阜県']
kinki = ['大阪府', '京都府', '兵庫県', '奈良県', '滋賀県', '和歌山県', '三重県']
tyugoku = ['鳥取県', '島根県', '岡山県', '広島県', '山口県']
sikoku = ['徳島県', '香川県', '愛媛県', '高知県']
kyushu = ['福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']


def jsonLoad(jsonName):
    loadJson = json.load(open(f'{jsonName}.json'))
    return loadJson


def twoDimeLs(ls):
    return list(map(list, set(map(tuple, ls))))


def judgeTikiKubun(jyo, ken):
    if jyo == "二ヶ村緑道":
        return ['関東', "東京", jyo]
    if ken in hokkaido:
        return ["北海道", ken, jyo]
    if ken in tohoku:
        return ["東北", ken, jyo]
    if ken in kanto:
        return ["関東", ken, jyo]
    if ken in hokuriku:
        return ["北陸", ken, jyo]
    if ken in tyuoKoti:
        return ["中央高地", ken, jyo]
    if ken in tokai:
        return ["東海", ken, jyo]
    if ken in kinki:
        return ["近畿", ken, jyo]
    if ken in tyugoku:
        return ["中国", ken, jyo]
    if ken in sikoku:
        return ["四国", ken, jyo]
    if ken in kyushu:
        return ["九州", ken, jyo]

    # 競艇
    # ['多摩川', '二ヶ村緑道']
tyohukuLs = []
cityDict = {}
shubetu = ['keirin', 'autorace', 'keiba', 'kyotei']
for s in shubetu:
    shubetuJson = jsonLoad(s)
    for i in shubetuJson.values():
        for j in i:
            cityDict[j['city']] = j['jyo']
            tyohukuLs.append([j['jyo'], j['city']])

tyohukuLsSet = twoDimeLs(tyohukuLs)
# pprint(tyohukuLsSet)
for i, j in tyohukuLsSet:
    print(i, j)
    cityDict['ken'] = j
    cityDict['jyo'] = i
    print(judgeTikiKubun(i, j))
