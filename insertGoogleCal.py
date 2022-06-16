from datetime import datetime
import googleapiclient.discovery
import google.auth
from pprint import pprint
import os
from dotenv import load_dotenv


def insertGoogleCal(title, startTime, endTime, colorId, calendarId):
    # .envファイルの内容を読み込見込む
    load_dotenv()

    # ①Google APIの準備をする
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    calendar_id = calendarId
    # Googleの認証情報をファイルから読み込む
    key_json_path = os.environ['key_json_path']
    gapi_creds = google.auth.load_credentials_from_file(key_json_path, SCOPES)[
        0]
    # APIと対話するためのResourceオブジェクトを構築する
    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=gapi_creds)

    # ②予定を書き込む
    # 書き込む予定情報を用意する
    body = {
        # 予定のタイトル
        'summary': title,
        # 予定の開始時刻
        'start': {
            'dateTime': startTime.isoformat(),
            'timeZone': 'Japan'
        },
        # 予定の終了時刻
        'end': {
            'dateTime': endTime.isoformat(),
            'timeZone': 'Japan'
        },
        'colorId': colorId
    }
    # 用意した予定を登録する
    event = service.events().insert(calendarId=calendar_id, body=body).execute()
    pprint(event)
