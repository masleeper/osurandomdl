from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt

class ManiaOptions(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mainLayout = QVBoxLayout()
        label = QLabel("Not yet available")
        mainLayout.addWidget(label)
        mainLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(mainLayout)