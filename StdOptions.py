from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from SlideEdit import SlideEdit
import APICaller

class StdOptions(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        self.findButton = QPushButton("Search")

        self.findButton.pressed.connect(self.validate)

        mainLayout.addWidget(self.lengthRow)
        mainLayout.addWidget(self.bpmRow)
        mainLayout.addWidget(self.minYearRow)
        mainLayout.addWidget(self.maxYearRow)
        mainLayout.addWidget(self.csRow)
        mainLayout.addWidget(self.hpRow)
        mainLayout.addWidget(self.odRow)
        mainLayout.addWidget(self.arRow)
        mainLayout.addWidget(self.srRow)
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

    def validate(self):
        APICaller.req()
