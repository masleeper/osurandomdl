from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from SlideEdit import SlideEdit
import re
import APICaller

class StdOptions(QWidget):
    def __init__(self, mapDisplay, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mapDisplay = mapDisplay
        mainLayout = QVBoxLayout()
        self.lengthRow = self.lineEditRow("Length")
        self.bpmRow = self.lineEditRow("BPM")
        self.minYearRow = self.lineEditRow("Minimum Year")
        self.maxYearRow = self.lineEditRow("Maximum Year")
        self.csRow = self.slideEditRow("Circle Size")
        self.hpRow = self.slideEditRow("HP")
        self.odRow = self.slideEditRow("Overall Difficulty")
        self.arRow = self.slideEditRow("Approach Rate")
        self.srRow = self.slideEditRow("Star Rating")
        self.leaderboardRow = self.leaderboardRow()
        self.findButton = QPushButton("Search")

        self.findButton.pressed.connect(self.search)

        mainLayout.addWidget(self.lengthRow)
        mainLayout.addWidget(self.bpmRow)
        mainLayout.addWidget(self.minYearRow)
        mainLayout.addWidget(self.maxYearRow)
        mainLayout.addWidget(self.csRow)
        mainLayout.addWidget(self.hpRow)
        mainLayout.addWidget(self.odRow)
        mainLayout.addWidget(self.arRow)
        mainLayout.addWidget(self.srRow)
        mainLayout.addWidget(self.leaderboardRow)
        mainLayout.addWidget(self.findButton)

        self.setLayout(mainLayout)

    def lineEditRow(self, text):
        hLayout = QHBoxLayout()
        label = QLabel(str(text))
        lineEdit = QLineEdit()
        includeRadButton = QRadioButton("include")

        includeRadButton.setChecked(True)

        hLayout.addWidget(label)
        hLayout.addWidget(lineEdit)
        hLayout.addWidget(includeRadButton)

        hLayout.setAlignment(Qt.AlignRight)

        widget = QWidget()
        widget.setLayout(hLayout)
        return widget

    def slideEditRow(self, text):
        hLayout = QHBoxLayout()
        hLayout.setAlignment(Qt.AlignRight)
        label = QLabel(str(text))
        slideEdit = SlideEdit()
        includeRadButton = QRadioButton("include")

        slideEdit.setAlignment(Qt.AlignRight)
        includeRadButton.setChecked(True)

        hLayout.addWidget(label)
        hLayout.addWidget(slideEdit)
        hLayout.addWidget(includeRadButton)

        widget = QWidget()
        widget.setLayout(hLayout)
        return widget

    def leaderboardRow(self):
        hLayout = QHBoxLayout()
        label = QLabel("Has Leaderboard")
        includeRadioButton = QRadioButton("include")
        includeRadioButton.setChecked(True)

        statLayout = QHBoxLayout()
        yesLeaderBoard = QRadioButton("Yes")
        yesLeaderBoard.setChecked(True)
        noLeaderBoard = QRadioButton("No")
        statLayout.addWidget(yesLeaderBoard)
        statLayout.addWidget(noLeaderBoard)
        statLayout.setAlignment(Qt.AlignLeft)
        statWidget = QWidget()
        statWidget.setLayout(statLayout)

        hLayout.addWidget(label)
        hLayout.addWidget(statWidget)
        hLayout.addWidget(includeRadioButton)
        widget = QWidget()
        widget.setLayout(hLayout)
        return widget

    def getLineEditText(self, lineEditRow):
        lineEdit = lineEditRow.children()[2]
        return lineEdit.text()

    def getSlideEditVal(self, slideEditRow):
        slideEdit = slideEditRow.children()[2]
        slider = slideEdit.children()[1]
        return slider.value()

    def isIncluded(self, row):
        includeRadio = row.children()[3]
        return includeRadio.isChecked()

    def invalidMsg(self, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Invalid Value")
        msgBox.setText(msg)
        msgBox.exec_()

    def search(self):
        params = self.validate()
        if not params["valid"]:
            return None
        else:
            print("Calling API")
            matchedMap = APICaller.getBeatMaps(params)
            if (matchedMap is None):
                print("Error finding map")
            else:
               self.mapDisplay.setMap(matchedMap)


    def validate(self):
        params = {"valid": True, "mode": 0}
        if self.isIncluded(self.lengthRow):
            try:
                length = int(self.getLineEditText(self.lengthRow))
                if length < 0:
                    params["valid"] = False
                    self.invalidMsg("Enter a positive value for length")
                    return params
                else:
                    params["length"] = length
            except:
                self.invalidMsg("Please enter an integer value for length")
                params["valid"] = False
                return params

        if self.isIncluded(self.bpmRow):
            try:
                bpm = float(self.getLineEditText(self.bpmRow))
                if bpm < 0:
                    params["valid"] = False
                    self.invalidMsg("Enter a positive value for BPM")
                    return params
                else:
                    params["bpm"] = bpm
            except:
                self.invalidMsg("Please enter a number for BPM")
                params["valid"] = False
                return params

        if self.isIncluded(self.minYearRow):
            minYearPattern = re.compile("^20(0[7-9]|[1-9][0-9])$")
            minYear = self.getLineEditText(self.minYearRow)
            if minYearPattern.match(minYear):
                params["minYear"] = int(minYear)
            else:
                params["valid"] = False
                self.invalidMsg("Invalid minimum year")
                return params

        if self.isIncluded(self.maxYearRow):
            maxYearPattern = re.compile("^20(0[7-9]|[1-9][0-9])$")
            maxYear = self.getLineEditText(self.maxYearRow)
            if maxYearPattern.match(maxYear):
                minYear = params["minYear"]
                if (minYear > int(maxYear)):
                    params["valid"] = False
                    self.invalidMsg("Minimum year greater than maximum year")
                    return params
                else:
                    params["maxYear"] = int(maxYear)
            else:
                params["valid"] = False
                self.invalidMsg("Invalid maximum year")
                return params

        if self.isIncluded(self.csRow):
            params["cs"] = self.getSlideEditVal(self.csRow)

        if self.isIncluded(self.hpRow):
            params["hp"] = self.getSlideEditVal(self.hpRow)

        if self.isIncluded(self.odRow):
            params["od"] = self.getSlideEditVal(self.odRow)

        if self.isIncluded(self.arRow):
            params["ar"] = self.getSlideEditVal(self.arRow)

        if self.isIncluded(self.srRow):
            params["sr"] = self.getSlideEditVal(self.srRow)

        if self.isIncluded(self.leaderboardRow):
            checkBoxes = self.leaderboardRow.children()[2].children()
            params["hasLeaderboard"] = checkBoxes[1].isChecked()

        return params
