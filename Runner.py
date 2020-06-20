from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import UI

app = QApplication([])
window = UI.MainWindow()
window.show()
app.exec_()