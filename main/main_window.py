from PyQt5.QtWidgets import  QMainWindow, QTabWidget


class MainWindow(QMainWindow):
    def __init__(self, views_tuple: tuple):
        super().__init__()
        self.views = views_tuple
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Serial Reader Rif corp.")
        self.setGeometry(100, 100, 600, 400)

        tabs = QTabWidget(self)
        self.setCentralWidget(tabs)
        for view in self.views:
            tabs.addTab(view, view.name)