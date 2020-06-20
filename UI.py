from PyQt5.QtWidgets import *
from SlideEdit import SlideEdit

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")
        sl = SlideEdit()

        layout = QHBoxLayout()
        layout.addWidget(sl)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

