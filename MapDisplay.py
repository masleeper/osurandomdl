from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import browser_cookie3
import requests

class MapDisplay(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mainLayout = QVBoxLayout()
        self.songLabel = QLabel("Song: --")
        self.artistLabel = QLabel("Artist: --")
        self.mapperLabel = QLabel("Mapper: --")
        self.diffLabel = QLabel("Difficulty Name: --")
        self.rankedLabel = QLabel("Ranked Status: --")
        self.downloadBtn = QPushButton("Download")

        self.downloadBtn.pressed.connect(self.download)
        mainLayout.addWidget(self.songLabel)
        mainLayout.addWidget(self.artistLabel)
        mainLayout.addWidget(self.mapperLabel)
        mainLayout.addWidget(self.diffLabel)
        mainLayout.addWidget(self.rankedLabel)
        mainLayout.addWidget(self.downloadBtn)

        self.setLayout(mainLayout)
        self.map = None

    def setMap(self, beatmap):
        self.map = beatmap
        self.songLabel.setText("Song: " + self.map.songTitle)
        self.artistLabel.setText("Artist: " + self.map.artist)
        self.mapperLabel.setText("Mapper: " + self.map.mapper)
        self.diffLabel.setText("Difficulty Name: " + self.map.diffName)
        rankedCodes = {
            -2: "Graveyard",
            -1: "WIP",
            0: "Pending",
            1: "Ranked",
            2: "Approved",
            3: "Qualified",
            4: "Loved"
        }
        self.rankedLabel.setText("Ranked Status: " + rankedCodes[self.map.rankedStatus])

    def download(self):
        # todo deal with windows restricted characters for filenames
        id = self.map.beatmapsetId
        cj = browser_cookie3.chrome(domain_name="ppy.sh")
        cstring = ""
        for cookie in cj:
            cstring += (cookie.name + "=" + cookie.value + "; ")
        headers = {
            "cookie": cstring,
            "referer": "https://osu.ppy.sh/beatmapsets"
        }

        resp = requests.get("https://osu.ppy.sh/beatmapsets/" + str(id) + "/download", headers=headers)
        for header in resp.headers:
            print(header, ": ", resp.headers[header])
        print("RESPONSE")
        contentDisposition = resp.headers["Content-Disposition"]
        filename = contentDisposition[contentDisposition.find("\"") + 1: -2]
        invalidChars = "<>:\"/\\|?*"
        print(filename)
        with open(filename, "wb") as f:
            f.write(resp.content)
