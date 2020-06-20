from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from DoubleSlider import DoubleSlider

class SlideEdit(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slider = DoubleSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(10)
        self.slider.setValue(5)

        self.lineEdit = QLineEdit()
        self.lineEdit.setText(str(self.slider.value()))
        self.lineEdit.setFixedWidth(40)
        self.lineEdit.setFixedHeight(20)

        self.slider.valueChanged.connect(lambda x: self.setLineEdit(self.slider.value()))
        self.lineEdit.textChanged.connect(lambda x: self.setSlider(self.lineEdit.text()))

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.lineEdit)
        self.setLayout(self.layout)

    def setSlider(self, value):
        try:
            self.slider.setValue(float(value))
        except:
            pass

    def setLineEdit(self, value):
        self.lineEdit.setText(str(value))
