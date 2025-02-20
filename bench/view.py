from PyQt5.QtWidgets import ( QCheckBox, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QComboBox, QSpinBox,
                            QTextEdit, QLabel, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal 
from PyQt5.QtSerialPort import QSerialPortInfo

from support.constants import Cmd

class BenchView(QWidget):
    connect_clicked = pyqtSignal(str, int)
    disconnect_clicked = pyqtSignal()
    command_sent = pyqtSignal(object, float)

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.name = "Bench"

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Connection controls
        port_layout = QHBoxLayout()
        self.port_combo = QComboBox()
        self.refresh_ports()
        self.baud_spin = QSpinBox()
        self.baud_spin.setRange(9600, 115200)
        self.baud_spin.setValue(115200)
        
        self.connect_btn = QPushButton("Connect")
        self.disconnect_btn = QPushButton("Disconnect")

        port_layout.addWidget(QLabel("Port:"))
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(QLabel("Baud:"))
        port_layout.addWidget(self.baud_spin)
        port_layout.addWidget(self.connect_btn)
        port_layout.addWidget(self.disconnect_btn)
        
        # Command controls
        cmd_layout = QHBoxLayout()
        self.cmd_combo = QComboBox()
        [self.cmd_combo.addItem(cmd.name) for cmd in Cmd]
        self.arg_input = QLineEdit("0")
        self.send_btn = QPushButton("Send Command")
        
        cmd_layout.addWidget(QLabel("Command:"))
        cmd_layout.addWidget(self.cmd_combo)
        cmd_layout.addWidget(QLabel("Argument:"))
        cmd_layout.addWidget(self.arg_input)
        cmd_layout.addWidget(self.send_btn)

        #Fast controls
        fast_controls_layout = QHBoxLayout()
        
        self.signal_enable = QCheckBox('Signal')
        self.power_enable = QCheckBox('Power')

        fast_controls_layout.addWidget(self.signal_enable)
        fast_controls_layout.addWidget(self.power_enable)

        # Data display
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addLayout(port_layout)
        layout.addLayout(cmd_layout)
        layout.addLayout(fast_controls_layout)
        layout.addWidget(self.log)


        # Signals
        self.connect_btn.clicked.connect(self.handle_connect)
        self.disconnect_btn.clicked.connect(self.disconnect_clicked.emit)
        self.send_btn.clicked.connect(self.handle_command)

        # Connection state start update
        self.disconnect_btn.setEnabled(False)
        self.cmd_combo.setEnabled(False)
        self.arg_input.setEnabled(False)
        self.send_btn.setEnabled(False)
        self.signal_enable.setEnabled(False)
        self.power_enable.setEnabled(False)


    def refresh_ports(self):
        self.port_combo.clear()
        
        ports = [port.portName() for port in QSerialPortInfo.availablePorts()]
        self.port_combo.addItems(ports)

    def handle_connect(self):
        port = self.port_combo.currentText()
        baud = self.baud_spin.value()
        self.connect_clicked.emit(port, baud)

    def handle_command(self):
        cmd_name = self.cmd_combo.currentText()
        cmd = next(c for c in Cmd if c.name == cmd_name)
        try:
            arg = float(self.arg_input.text())
            self.command_sent.emit(cmd, arg)
        except ValueError:
            self.log.append("Invalid argument!")

    def update_connection_state(self, connected):
        self.connect_btn.setEnabled(not connected)
        self.disconnect_btn.setEnabled(connected)
        self.port_combo.setEnabled(not connected)
        self.baud_spin.setEnabled(not connected)
        self.cmd_combo.setEnabled(connected)
        self.arg_input.setEnabled(connected)
        self.send_btn.setEnabled(connected)
        self.signal_enable.setEnabled(connected)
        self.power_enable.setEnabled(connected)

    def log_data(self, data):
        self.log.append(f"Received: {str(data)}")

    def show_error(self, message):
        self.log.append(f"Error: {message}")