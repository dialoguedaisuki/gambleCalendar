from util import *
import sys

print(sys.argv)
kaisaiMouth = sys.argv[1]
kaisaiYear = sys.argv[2]
shubetuFlag = sys.argv[3]
print(kaisaiMouth, kaisaiYear, shubetuFlag)

if shubetuFlag == "keiba":
    jsonRawKeiba = netkeibaGetCal(
        f'https://nar.netkeiba.com/top/calendar.html?year={kaisaiYear}&month={kaisaiMouth}', kaisaiMouth)
    jsonDump(jsonRawKeiba, 'keiba.json')

if shubetuFlag == "keirin":
    keirinJson = netkeirinSc(
        f'https://keirin.netkeiba.com/race/race_calendar/?kaisai_year={kaisaiYear}&kaisai_month={kaisaiMouth}')
    jsonDump(keirinJson, 'keirin.json')

if shubetuFlag == "kyotei":
    autoRaceBaseurl = "https://www.oddspark.com/autorace/KaisaiRaceList.do?raceDy="
    autoRaceLs = MouthUrlParser(
        autoRaceBaseurl, autoRaceGetCal, kaisaiMouth, kaisaiYear)
    jsonDump(autoRaceLs, 'autorace.json')

if shubetuFlag == "autorace":
    kyoteiBaseUrl = "https://www.boatrace.jp/owpc/pc/race/index?hd="
    kyoteiLs = MouthUrlParser(
        kyoteiBaseUrl, kyoteiGetCal, kaisaiMouth, kaisaiYear)
    jsonDump(kyoteiLs, 'kyotei.json')

if shubetuFlag == "all":
    jsonRawKeiba = netkeibaGetCal(
        f'https://nar.netkeiba.com/top/calendar.html?year={kaisaiYear}&month={kaisaiMouth}', kaisaiMouth)
    jsonDump(jsonRawKeiba, 'keiba.json')
    keirinJson = netkeirinSc(
        f'https://keirin.netkeiba.com/race/race_calendar/?kaisai_year={kaisaiYear}&kaisai_month={kaisaiMouth}')
    jsonDump(keirinJson, 'keirin.json')
    autoRaceBaseurl = "https://www.oddspark.com/autorace/KaisaiRaceList.do?raceDy="
    autoRaceLs = MouthUrlParser(
        autoRaceBaseurl, autoRaceGetCal, kaisaiMouth, kaisaiYear)
    jsonDump(autoRaceLs, 'autorace.json')
    kyoteiBaseUrl = "https://www.boatrace.jp/owpc/pc/race/index?hd="
    kyoteiLs = MouthUrlParser(
        kyoteiBaseUrl, kyoteiGetCal, kaisaiMouth, kaisaiYear)
    jsonDump(kyoteiLs, 'kyotei.json')
