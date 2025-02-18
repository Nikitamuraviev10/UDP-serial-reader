from PyQt5.QtCore import QThread, pyqtSignal
import socket
from support.c_deserial import Deserial
import data_setter
from support.event_timer import EventTimer
import time
from support.constants import data_struct


class ReceiverThread(QThread):
    update_trigger = pyqtSignal()
    log_signal = pyqtSignal(bytes)

    def __init__(self, ip, port, setter):
        super().__init__()
        self.ip = ip
        self.port = port
        self.setter = setter
        self.deserial = Deserial(data_struct)
        self.running = True

        # Связываем сигналы
        self.update_trigger.connect(self.handle_update)
        self.log_signal.connect(setter.log_data)

        self.et = EventTimer()
        self.et.add(0.05, lambda: self.update_trigger.emit())

    def handle_update(self):
        try:
            data: bytes = self.last_data
            data_dict = self.deserial.to_dict(data)
            
            for key in data_dict.keys():
                if hasattr(self.setter, key):
                    getattr(self.setter, key)(data_dict[key])
            
            self.setter.update()
        except Exception as e:
            print(e)

    def run(self):
        bufferSize = 1024
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))

        while self.running:
            data, addr = sock.recvfrom(bufferSize)
            self.last_data = data
            self.log_signal.emit(data)
            self.et.handle(time.time(), args=(data,))

        sock.close()

    def stop(self):
        self.running = False
        self.wait()


def start(ip, port, setter):
    thread = ReceiverThread(ip, port, setter)
    thread.start()
    return thread