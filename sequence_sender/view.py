import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                            QTextEdit, QFileDialog, QMessageBox,
                            QComboBox)  # Добавили импорт QComboBox
from PyQt5.QtCore import pyqtSignal

class SequenceSenderView(QWidget):
    file_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.name = "Отправитель последовательности"
        self.sequences_folder = "sequences_folder" 
        self.update_yaml_list()  
        
    def init_ui(self):
        self.layout = QVBoxLayout()
        

        self.cb_yaml_files = QComboBox()
        

        self.btn_send = QPushButton('Отправить выбранный файл')
        self.btn_send.clicked.connect(self.send_selected_file)
        
        self.btn_open = QPushButton('Открыть конфиг')
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        
        self.layout.addWidget(self.cb_yaml_files)
        self.layout.addWidget(self.btn_send)
        self.layout.addWidget(self.btn_open)
        self.layout.addWidget(self.output_area)
        
        self.setLayout(self.layout)
        self.btn_open.clicked.connect(self.open_file_dialog)

    def update_yaml_list(self):
        self.cb_yaml_files.clear()
        
        if not os.path.exists(self.sequences_folder):
            return
            
        files = [f for f in os.listdir(self.sequences_folder)
                if f.endswith(('.yaml', '.yml'))]
                
        for file in sorted(files):
            self.cb_yaml_files.addItem(file)

    def send_selected_file(self):
        if self.cb_yaml_files.count() == 0:
            self.show_error("Нет доступных конфигурационных файлов")
            return
            
        selected_file = self.cb_yaml_files.currentText()
        full_path = os.path.join(self.sequences_folder, selected_file)
        
        if os.path.exists(full_path):
            self.file_selected.emit(full_path)
        else:
            self.show_error("Файл больше не существует!")

    def open_file_dialog(self):
        start_dir = os.path.abspath(self.sequences_folder)
        path, _ = QFileDialog.getOpenFileName(
            self, 'Открыть конфиг', start_dir,
            'YAML Files (*.yaml *.yml)')
            
        if path:
            self.file_selected.emit(path)
            self.update_yaml_list()  

    def update_output(self, text: str):
        self.output_area.append(text)

    def show_error(self, message: str):
        QMessageBox.critical(self, 'Error', message)
