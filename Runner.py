from PyQt5.QtWidgets import QApplication
import UI

app = QApplication([])
window = UI.MainWindow()
window.show()
app.exec_()