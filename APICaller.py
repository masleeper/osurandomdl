from click import option
import requests
import time
import datetime
import concurrent.futures
import threading
from Beatmap import Beatmap
from random import random, seed
from random import randint

def getBeatMaps(options):
    # todo: don't put api key in code, store it somewhere secure in final version

    minYear = options["minYear"] if "minYear" in options.keys() else 2007
    currentYear = datetime.datetime.now().year
    maxYear = options["maxYear"] if "maxYear" in options.keys() else currentYear
    specMap = Beatmap(options)
    print(specMap)
    # if specMap.hasLeaderboard:
    #     return findRanked(specMap, minYear, maxYear)
    # else:
    #     return findUnranked(specMap, minYear, maxYear)

rankedList = []
lstMinYear = 2007
lstMaxYear = datetime.datetime.now().year
def findRanked(options, minYear,  maxYear):
    global lstMinYear, lstMaxYear
    if len(rankedList) == 0:
        lstMinYear = minYear
        lstMaxYear = maxYear
        buildRankedList(list(range(minYear, maxYear + 1)))
    else:
        if minYear != lstMinYear or maxYear != lstMaxYear:
            yearList = list()
            if minYear < lstMinYear:
                yearList.extend(range(minYear, lstMinYear))
                lstMinYear = minYear
            if maxYear > lstMaxYear:
                yearList.extend(range(lstMaxYear + 1, maxYear + 1))
                lstMaxYear = maxYear
            buildRankedList(yearList)
    seed(time.time())
    mapNum = randint(0, len(rankedList) - 1)
    randomMap = rankedList[mapNum]
    attempts = 0
    while not randomMap.compare(options):
        if attempts >= 500:
            return None
        mapNum = randint(0, len(rankedList) - 1)
        randomMap = rankedList[mapNum]
        attempts += 1
    return randomMap


def buildRankedList(yearList):
    global rankedList
    rankedSet = set(rankedList)
    rankedLock = threading.Lock()
    numThreads = len(yearList)

    with concurrent.futures.ThreadPoolExecutor(max_workers=numThreads) as executor:
        for year in yearList:
            executor.submit(yearMapGet, year, rankedSet, rankedLock)

    rankedList = list(rankedSet)

def yearMapGet(year, rankedSet, lock):
    key = ""
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

def findUnranked(options, minYear, maxYear):
    key = ""
    queryParams = {"k": key}
    url = "https://osu.ppy.sh/api/get_beatmaps"
    maxSetId = int(requests.get(url, queryParams).json()[-1]["beatmapset_id"])

    seed(time.time())
    attempts = 0
    randomMap = Beatmap(dict())
    while not randomMap.compare(options):
        if attempts >= 500:
            return None
        attempts += 1
        randomSetId = randint(0, maxSetId)
        queryParams["s"] = randomSetId

        try:
            response = requests.get(url, params=queryParams)
            time.sleep(.100)
        except:
            # API call failed
            return None

        if response.text != "[]":
            resp = response.json()

            for beatMap in resp:
                mapDict = apiToLocal(beatMap)
                randomMap = Beatmap(mapDict)

                if randomMap.compare(options):
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
