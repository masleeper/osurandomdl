from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QValidator


class MinValidator(QValidator):

    def __init__(self, minVal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minVal = minVal if (isinstance(minVal, int) or isinstance(minVal, float)) else 0

    def validate(self, val, pos):
        try:
            num = int(val) if isinstance(self.minVal, int) else float(val)
            if num >= self.minVal:
                return (QValidator.Acceptable, val, pos)
            else:
                return (QValidator.Invalid, val, pos)
        except:
            if isinstance(self.minVal, float):
                if val[-1] == '.':
                    return (QValidator.Intermediate, val, pos)
            return (QValidator.Invalid, val, pos)


class MaxValidator(QValidator):

    def __init__(self, maxVal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxVal = maxVal if (isinstance(maxVal, int) or isinstance(maxVal, float)) else 0

    def validate(self, val, pos):
        try:
            num = int(val) if isinstance(self.maxVal, int) else float(val)
            if num <= self.maxVal:
                return (QValidator.Acceptable, val, pos)
            else:
                return (QValidator.Invalid, val, pos)
        except:
            if isinstance(self.maxVal, float):
                if val[-1] == '.':
                    return (QValidator.Intermediate, val, pos)
            return (QValidator.Invalid, val, pos)


class MinMaxEdit(QWidget):

    def __init__(self, name, minVal, maxVal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.minVal = minVal
        self.maxVal = maxVal
        self.layout = QHBoxLayout()

        self.minEdit = QLineEdit()
        self.minEdit.setPlaceholderText("Min")
        # self.minValidator = MinValidator(minVal)
        # self.minEdit.setValidator(self.minValidator)

        self.maxEdit = QLineEdit()
        self.maxEdit.setPlaceholderText("Max")
        # self.maxValidator = MaxValidator(maxVal)
        # self.maxEdit.setValidator(self.maxValidator)

        self.layout.addWidget(self.minEdit)
        self.layout.addWidget(self.maxEdit)
        self.layout.setAlignment(Qt.AlignRight)
        self.setLayout(self.layout)

    def validate(self):
        if not (self.minEdit.text().isnumeric() and self.maxEdit.text().isnumeric()):
            return False
        return self.getMinValEntered() <= self.getMaxValEntered()

    def getMinValEntered(self):
        return int(self.minEdit.text()) if isinstance(self.minVal, int) else float(self.minEdit.text())

    def getMaxValEntered(self):
        return int(self.maxEdit.text()) if isinstance(self.maxVal, int) else float(self.maxEdit.text())

    # def getMinValidator(self):
    #     return self.minValidator
    #
    # def getMaxValidator(self):
    #     return self.maxValidator




