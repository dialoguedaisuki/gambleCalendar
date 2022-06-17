import json
from pprint import pprint


def jsonLoad(jsonName):
    loadJson = json.load(open(f'{jsonName}.json'))
    return loadJson


keirin = jsonLoad('keirin')
for i in keirin.values():
    for j in i:
        print(j['jyo'], j['city'])
