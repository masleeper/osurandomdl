from typing import NewType

def store(lst):
    separator = ","
    with open("cache.csv", mode="w") as file:
        for map in lst:
            line = ""
            line += str(map.beatmapId) + separator
            line += str(map.beatmapsetId) + separator
            line += str(map.year) + separator
            line += str(map.cs) + separator
            line += str(map.hp) + separator
            line += str(map.ar) + separator
            line += str(map.sr) + separator
            line += str(map.bpm) + separator
            line += str(map.length) + separator
            line += str(map.artist) + separator
            line += str(map.mapper) + separator
            line += str(map.songTitle) + separator
            line += str(map.diffName) + separator
            line += str(map.mode) + separator
            line += str(map.rankedStatus) + separator
            line += str(map.hasLeaderboard)
            file.write(line)
            file.write("\n")



def retrieve():
    pass