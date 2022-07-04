# オケラカレンダー
## カレンダー
- [競技別オケラカレンダー](https://dialoguedaisuki.github.io/gambleCalendar/)
- [地域別オケラカレンダー]()

## 使い方
- Jsonを取得する
```bash
# 例
python getJson 7 2022 keiba/keirin/kyotei/autorace
```

- GoogleカレンダーからAPI経由で予定登録できるようにする
  - サービスアカウント作って対応させる
  - key.json,setting.iniを作って同一ディレクトリに入れる

- Googleカレンダーに登録する
```bash
# 例
python jsonToCal.py keiba/keirin/kyotei/autorace
```

- Googleカレンダーの予定を削除する
  - 指定した日を起点に現在まで全部削除する
```bash
# 例
python deleteUtil.py keiba/keirin/kyotei/autorace 2022 7 1 $dryrunOption
```

- 地域別csv作成
```bash
# 例
python createUtilJson.py
```