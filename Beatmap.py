class Beatmap:
    def __init__(self, params):
        self.cs = float(params["Circle Size"]) if "Circle Size" in params.keys() else -1
        self.hp = float(params["HP"]) if "HP" in params.keys() else -1
        self.ar = float(params["Approach Rate"]) if "Approach Rate" in params.keys() else -1
        self.sr = float(params["Star Rating"]) if "Star Rating" in params.keys() else -1
        self.od = float(params["Overall Difficulty"]) if "Overall Difficulty" in params.keys() else -1
        self.bpm = float(params["BPM"]) if "BPM" in params.keys() else -1
        self.year = int(params["Year"]) if "Year" in params.keys() else -1
        self.length = int(params["Length"]) if "Length" in params.keys() else -1
        self.beatmapId = int(params["beatmapId"]) if "beatmapId" in params.keys() else -1
        self.beatmapsetId = int(params["beatmapsetId"]) if "beatmapsetId" in params.keys() else -1
        self.artist = params["artist"] if "artist" in params.keys() else None
        self.mapper = params["creator"] if "creator" in params.keys() else None
        self.songTitle = params["title"] if "title" in params.keys() else None
        self.diffName = params["diffName"] if "diffName" in params.keys() else None
        self.rankedStatus = int(params["rankedStatus"]) if "rankedStatus" in params.keys() else -3
        self.mode = int(params["mode"]) if "mode" in params.keys() else -1

        if "hasLeaderboard" in params.keys():
            if self.rankedStatus < -2:
                self.hasLeaderboard = params["hasLeaderboard"]
            else:
                self.hasLeaderboard = self.rankedStatus >= 1
        else:
            self.hasLeaderboard = self.rankedStatus >= 1

    def __str__(self):
        print("mode: ", self.mode)
        print("length: ", self.length)
        print("bpm: ", self.bpm)
        print("cs: ", self.cs)
        print("hp: ", self.hp)
        print("od: ", self.od)
        print("ar: ", self.ar)
        print("sr: ", self.sr)
        print("map id: ", self.beatmapId)
        print("set id: ", self.beatmapsetId)
        print("artist: ", self.artist)
        print("song title: ", self.songTitle)
        print("mapper: ", self.mapper)
        print("year: ", self.year)
        print("diff name: ", self.diffName)
        print("ranked status: ", self.rankedStatus)
        print("has leaderboard: ", self.hasLeaderboard)

    def __eq__(self, obj):
        """
        This function compares length, bpm, cs, hp, od, ar, sr, and year and returns true if they match.
        However, if this Beatmap's value for a parameter is -1 or None, then that indicates that this map
        will not use those parameters for comparison.
        :param obj: Other map to be compared
        :return: True if comparable values match, false otherwise.
        """

        if not isinstance(obj, Beatmap):
            return False

        if self.mode != obj.mode and self.mode != -1:
            return False

        if self.length != obj.length and self.length != -1:
            return False

        if self.bpm != obj.bpm and self.bpm != -1:
            return False

        if self.cs != obj.cs and self.cs != -1:
            return False

        if self.hp != obj.hp and self.hp != -1:
            return False

        if self.od != obj.od and self.od != -1:
            return False

        if self.ar != obj.ar and self.ar != -1:
            return False

        if self.sr != obj.sr and self.sr != -1:
            return False

        if self.hasLeaderboard != obj.hasLeaderboard:
            return False

        return True

    def __hash__(self):
        return self.beatmapId

    def compare(self,params):
        pass