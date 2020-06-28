from PyQt5.QtWidgets import *
from PyQt5.Qt import *

class MapDisplay(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mainLayout = QVBoxLayout()
        songLabel = QLabel("Song: --")
        artistLabel = QLabel("Artist: --")
        mapperLabel = QLabel("Mapper: --")
        diffLabel = QLabel("Difficulty Name: --")
        rankedLabel = QLabel("Ranked: --")

        mainLayout.addWidget(songLabel)
        mainLayout.addWidget(artistLabel)
        mainLayout.addWidget(mapperLabel)
        mainLayout.addWidget(diffLabel)
        mainLayout.addWidget(rankedLabel)

        self.setLayout(mainLayout)
