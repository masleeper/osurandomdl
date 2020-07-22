import requests
import time
import datetime
import concurrent.futures
import threading
from Beatmap import Beatmap
from random import seed
from random import randint

def getBeatMaps(options):
    # todo: don't put api key in code, store it somewhere secure in final version

    minYear = options["minYear"] if "minYear" in options.keys() else 2007
    currentYear = datetime.datetime.now().year
    maxYear = options["maxYear"] if "maxYear" in options.keys() else currentYear
    key = "get yer own key"
    queryParams = {"k": key}
    url = "https://osu.ppy.sh/api/get_beatmaps"
    specMap = Beatmap(options)
    if specMap.hasLeaderboard:
        return findRanked(specMap, minYear, maxYear)
    else:
        return findUnranked(specMap, minYear, maxYear)

rankedList = []
def findRanked(specMap, minYear,  maxYear):
    # todo may need to adjust if statement based on year input
    if len(rankedList) == 0:
        buildRankedList(minYear, maxYear)
    seed(time.time())
    mapNum = randint(0, len(rankedList) - 1)
    randomMap = rankedList[mapNum]
    while not specMap == randomMap:
        mapNum = randint(0, len(rankedList) - 1)
        randomMap = rankedList[mapNum]
    return randomMap


def buildRankedList(minYear, maxYear):
    rankedSet = set()
    rankedLock = threading.Lock()
    numThreads = (maxYear - minYear) + 1
    print("num threads: ", numThreads)
    with concurrent.futures.ThreadPoolExecutor(max_workers=numThreads) as executor:
        for year in range(minYear, maxYear + 1):
            executor.submit(yearMapGet, year, rankedSet, rankedLock)
    global rankedList
    rankedList = list(rankedSet)

def yearMapGet(year, rankedSet, lock):
    key = "get yer own key"
    queryParams = {"k": key}
    url = "https://osu.ppy.sh/api/get_beatmaps"
    for month in range(1, 13):
        since = datetime.datetime(year, month, 1).strftime("%Y-%m-%d %H:%M:%S")
        queryParams["since"] = since
        response = requests.get(url, params=queryParams).json()
        for mapJson in response:
            mapDict = apiToLocal(mapJson)
            beatmap = Beatmap(mapDict)
            with lock:
                rankedSet.add(beatmap)

def findUnranked(specMap, minYear, maxYear):
    key = "get yer own key"
    queryParams = {"k": key}
    url = "https://osu.ppy.sh/api/get_beatmaps"
    maxSetId = int(requests.get(url, queryParams).json()[-1]["beatmapset_id"])

    seed(time.time())
    numcalls = 0
    randomMap = Beatmap(dict())
    while not specMap.match(randomMap):
        if numcalls >= 200:
            print("calls exceeded")
            break
        numcalls += 1
        randomSetId = randint(0, maxSetId)
        queryParams["s"] = randomSetId
        # print(randomSetId)

        try:
            response = requests.get(url, params=queryParams)
            time.sleep(.100)
        except:
            print("API call failed")
            return None
        # print(response.text)
        if response.text != "[]":
            resp = response.json()

            for beatMap in resp:
                mapDict = apiToLocal(beatMap)
                randomMap = Beatmap(mapDict)
                # print(randomMap.toString())
                if specMap == randomMap:
                    if minYear <= randomMap.year <= maxYear:
                        return randomMap


def apiToLocal(apiJson):
    ret = {}
    for key in apiJson.keys():
        value = apiJson[key]
        if key == "beatmap_id":
            ret["beatmapId"] = value
        elif key == "beatmapset_id":
            ret["beatmapsetId"] = value
        elif key == "diff_size":
            ret["cs"] = value
        elif key == "diff_overall":
            ret["od"] = value
        elif key == "diff_approach":
            ret["ar"] = value
        elif key == "diff_drain":
            ret["hp"] = value
        elif key == "difficultyrating":
            ret["sr"] = value
        elif key == "approved":
            ret["rankedStatus"] = value
        elif key == "total_length":
            ret["length"] = value
        elif key == "version":
            ret["diffName"] = value
        elif key == "submit_date":
            ret["year"] = int(value[0:4])
        else:
            ret[key] = value
    return ret
