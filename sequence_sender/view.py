from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QTextEdit, QFileDialog, QMessageBox)
from PyQt5.QtCore import pyqtSignal

class SequenceSenderView(QWidget):
    file_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.name = "Sequence Sender"
        
    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.btn_open = QPushButton('Open Config')
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        
        self.layout.addWidget(self.btn_open)
        self.layout.addWidget(self.output_area)
        self.setLayout(self.layout)
        
        self.btn_open.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 'Open Config', '', 'YAML Files (*.yaml *.yml)')
        if path:
            self.file_selected.emit(path)

    def update_output(self, text: str):
        self.output_area.append(text)

    def show_error(self, message: str):
        QMessageBox.critical(self, 'Error', message)