class Beatmap:
    def __init__(self, params):
        self.cs = float(params["cs"]) if "cs" in params.keys() else -1
        self.hp = float(params["hp"]) if "hp" in params.keys() else -1
        self.ar = float(params["ar"]) if "ar" in params.keys() else -1
        self.sr = float(params["sr"]) if "sr" in params.keys() else -1
        self.od = float(params["od"]) if "od" in params.keys() else -1
        self.bpm = float(params["bpm"]) if "bpm" in params.keys() else -1
        self.year = int(params["year"]) if "year" in params.keys() else -1
        self.length = int(params["length"]) if "length" in params.keys() else -1
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
        ret = ""
        ret += f'mode: {self.mode}\n'
        ret += f'length: {self.length}\n'
        ret += f'bpm: {self.bpm}\n'
        ret += f'cs: {self.cs}\n'
        ret += f'hp: {self.hp}\n'
        ret += f'od: {self.od}\n'
        ret += f'ar: {self.ar}\n'
        ret += f'sr: {self.sr}\n'
        ret += f'map id: {self.beatmapId}\n'
        ret += f'set id: {self.beatmapId}\n'
        ret += f'artist: {self.artist}\n'
        ret += f'song title: {self.songTitle}\n'
        ret += f'mapper: {self.mapper}\n'
        ret += f'year: {self.year}\n'
        ret += f'diff name: {self.diffName}\n'
        ret += f'ranked status: {self.rankedStatus}\n'
        ret += f'has leaderboard: {self.hasLeaderboard}\n'
        return ret

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
        if not self._checkRange("Circle Size", self.cs, params):
            return False
        if not self._checkRange("HP",self.hp, params):
            return False
        if not self._checkRange("Length", self.length, params):
            return False
        if not self._checkRange("BPM", self.bpm, params):
            return False
        if not self._checkRange("Year", self.year, params):
            return False
        if not self._checkRange("Overall Difficulty", self.od, params): 
            return False
        if not self._checkRange("Approach Rate", self.ar, params):
            return False
        if not self._checkRange("Star Rating", self.sr, params):
            return False
        if not self.hasLeaderboard == params["hasLeaderboard"]:
            return False
        if not self.mode == params["mode"]:
            return False
        return True

    def _checkRange(self, key, value, params):
        if key in params.keys():
            low,high = params[key]
            return low <= value <= high
        return True