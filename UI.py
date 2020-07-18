from PyQt5.QtWidgets import *
from StdOptions import StdOptions
from ManiaOptions import ManiaOptions
from CtbOptions import CtbOptions
from TaikoOptions import TaikoOptions
from MapDisplay import MapDisplay

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Osu Random Map Downloader")

        mainLayout = QHBoxLayout()

        self.tabs = QTabWidget()
        self.mapDisplay = MapDisplay()

        # tabs for each game mode
        self.stdOptions = StdOptions(self.mapDisplay)
        self.maniaOptions = ManiaOptions()
        self.ctbOptions = CtbOptions()
        self.taikoOptions = TaikoOptions()
        self.tabs.addTab(self.stdOptions, "Standard")
        self.tabs.addTab(self.maniaOptions, "Mania")
        self.tabs.addTab(self.ctbOptions, "Catch the Beat")
        self.tabs.addTab(self.taikoOptions, "Taiko")

        mainLayout.addWidget(self.tabs)
        mainLayout.addWidget(self.mapDisplay)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
