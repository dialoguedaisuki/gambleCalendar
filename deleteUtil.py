import datetime
import re
import googleapiclient.discovery
import google.auth
import configparser
from pprint import pprint
from datetime import datetime as dt


def auth_cal_id(envName):
    config = configparser.ConfigParser()
    config.read('setting.ini')
    calId = config.get(envName, 'calId')
    return calId


def strToDatetime(str):
    rawStr = re.search(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]', str).group()
    ifLs = rawStr.split('-')
    return ifLs


def delYotei(eventId):
    result = service.events().delete(calendarId=calendar_id, eventId=eventId).execute()
    return result


# ①Google APIの準備をする
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = auth_cal_id("kyotei")
# Googleの認証情報をファイルから読み込む
gapi_creds = google.auth.load_credentials_from_file(
    'key.json', SCOPES)[0]
# APIと対話するためのResourceオブジェクトを構築する
service = googleapiclient.discovery.build(
    'calendar', 'v3', credentials=gapi_creds)


# 削除する機関の頭を決定する
now = datetime.datetime(2022, 7, 1).isoformat() + 'Z'
# 今日いこう
#now = datetime.datetime.utcnow().isoformat() + 'Z'
event_list = service.events().list(
    calendarId=calendar_id, timeMin=now,
    maxResults=10000, singleEvents=True,
    orderBy='startTime').execute()
countLs = []
for i in event_list['items']:
    pprint(i)
    countLs.append(i)
    rawDate = i['start']['dateTime']
    print(i['start']['dateTime'])
    ifLs = strToDatetime(rawDate)
    # delYotei(i['id'])
print(len(countLs))
event_id = ""
# 削除実行
# service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

# Dry Run　オプションをつける
