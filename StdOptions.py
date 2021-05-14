from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QWidget, QRadioButton, QMessageBox
from PyQt5.QtCore import Qt
from SlideEdit import SlideEdit
from MinMaxEdit import *
import re
import APICaller

class StdOptions(QWidget):
    # todo cache ranked list on application close
    def __init__(self, mapDisplay, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.includeList = []
        self.mapDisplay = mapDisplay
        mainLayout = QVBoxLayout()
        self.lengthRow = self.minMaxRow(0, 10000, "Length")
        self.bpmRow = self.minMaxRow(0, 1000, "BPM")
        self.YearRow = self.minMaxRow(2007, 2021, "Year")
        self.csRow = self.minMaxRow(0.0, 10.0, "Circle Size")
        self.hpRow = self.minMaxRow(0.0, 10.0, "HP")
        self.odRow = self.minMaxRow(0.0, 10.0, "Overall Difficulty")
        self.arRow = self.minMaxRow(0.0, 10.0, "Approach Rate")
        self.srRow = self.minMaxRow(0.0, 10.0,"Star Rating")
        self.leaderboardRow = self.leaderboardRow()
        self.findButton = QPushButton("Search")

        self.findButton.pressed.connect(self.search)

        mainLayout.addWidget(self.lengthRow)
        mainLayout.addWidget(self.bpmRow)
        mainLayout.addWidget(self.YearRow)
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
        lineEdit.setPlaceholderText(text)
        includeRadButton = QRadioButton("include")

        includeRadButton.setChecked(True)

        hLayout.addWidget(label)
        hLayout.addWidget(lineEdit)
        hLayout.addWidget(includeRadButton)

        hLayout.setAlignment(Qt.AlignRight)

        widget = QWidget()
        widget.setLayout(hLayout)
        return widget

    def minMaxRow(self, minVal, maxVal, text):
        hLayout = QHBoxLayout()
        hLayout.setAlignment(Qt.AlignRight)
        label = QLabel(str(text))

        minMaxRow = MinMaxEdit(text, minVal, maxVal)
        includeRadButton = QRadioButton("include")
        includeRadButton.pressed.connect(lambda: self.addToInclude(minMaxRow))

        hLayout.addWidget(label)
        hLayout.addWidget(minMaxRow)
        hLayout.addWidget(includeRadButton)

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
        numChildren = len(row.children())
        includeRadio = row.children()[numChildren - 1]
        return includeRadio.isChecked()

    def invalidMsg(self, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Invalid Value")
        msgBox.setText(msg)
        msgBox.exec_()

    def addToInclude(self, widget):
        if self.includeList.count(widget) == 0:
            self.includeList.append(widget)
        else:
            self.includeList.remove(widget)

    def search(self):
        params = self.validate()
        if not params["valid"]:
            msg = QMessageBox()
            msg.setWindowTitle("Invalid input")
            msg.setText("Invalid search parameter, check to make sure they're correct")
            msg.exec_()
            return None
        else:
            print("Calling API")
            matchedMap = APICaller.getBeatMaps(params)
            if matchedMap is None:
                msg = QMessageBox()
                msg.setWindowTitle("No Match Found")
                msg.setText("500 attempts were made at finding a matching map and one wasn't found."
                            "Try again or change search parameters.")
                msg.exec_()
            else:
                self.mapDisplay.setMap(matchedMap)


    def validate(self):
        params = {"valid": True, "mode": 0}
        for minmax in self.includeList:
            if minmax.validate():
                params[minmax.name] = [minmax.getMinValEntered(), minmax.getMaxValEntered()]
                # print(f"{minmax.minEdit.text()} {minmax.maxEdit.text()}")
            else:
                params["valid"] = False
                print("row invalid")
                break

        if self.isIncluded(self.leaderboardRow):
            checkBoxes = self.leaderboardRow.children()[2].children()
            params["hasLeaderboard"] = checkBoxes[1].isChecked()

        return params