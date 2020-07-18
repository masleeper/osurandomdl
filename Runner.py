from PyQt5.QtWidgets import *
import UI

app = QApplication([])
window = UI.MainWindow()
window.show()
app.exec_()