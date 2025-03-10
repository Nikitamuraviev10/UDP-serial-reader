from PyQt5.QtCore import QEventLoop, QObject, QTimer, pyqtSignal, QThread, QMutex, QMutexLocker
from PyQt5.QtSerialPort import QSerialPort
import struct

from support.constants import Cmd, Status


class BenchWorker(QObject):
    data_processed = pyqtSignal(object)
    command_result = pyqtSignal(object)
    done_signal = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.serial = QSerialPort()
        self.serial.readyRead.connect(self.handle_ready_read)
        self.mutex = QMutex()
        self.running = False
        self.out_f = None
        self.last_response = None
        self.response_received = False

    def connect_serial(self, port, baudrate):
        self.serial.setPortName(port)
        self.serial.setBaudRate(baudrate)
        if self.serial.open(QSerialPort.ReadWrite):
            self.running = True
            return True
        self.error_occurred.emit(self.serial.errorString())
        return False

    def disconnect_serial(self):
        self.running = False
        if self.serial.isOpen():
            self.serial.close()

    def handle_ready_read(self):
        while self.serial.bytesAvailable() >= 12:
            data = self.serial.read(12)
            if len(data) != 12:
                continue

            if int.from_bytes(data[:2], 'little') == 0xAAAA:
                status = self.get_status(data)
                self.process_packet(status)

    def process_packet(self, response):
        cmd_id, status = response

        if cmd_id == Cmd.Start and status == Status.Done:
            self.done_signal.emit()

        self.last_response = status
        self.response_received = True
        self.command_result.emit(status)

        self.data_processed.emit(response)

    def send_command(self, cmd, arg):
        try:
            self.last_response = None
            self.response_received = False

            data = self.serialize(cmd, arg)
            with QMutexLocker(self.mutex):
                self.serial.write(data)
                if not self.serial.waitForBytesWritten(500):
                    raise TimeoutError("Write timeout")

            timer = QTimer()
            timer.setSingleShot(True)

            loop = QEventLoop()

            timer.timeout.connect(loop.quit)
            self.command_result.connect(loop.quit)

            timer.start(300)
            loop.exec_()

            if not self.response_received:
                raise TimeoutError("No response received within timeout")

            return self.last_response

        except Exception as e:
            self.error_occurred.emit(str(e))
            raise


    def get_status(self, data):
        head, cmd, status, crc = struct.unpack('HHLL', data)
        cmd = Cmd(cmd)
        if cmd.value >= 2048:
            head, cmd, val, crc = struct.unpack('HHfL', data)
            return cmd, val

        return cmd, Status(status)

    def serialize(self, cmd, arg):
        head = 0xAAAA
        cmd = cmd.value

        if(isinstance(arg, float)):
            format_ = '<HHf'
            arg = float(arg)
        elif(isinstance(arg, int)):
            format_ = '<HHl'
            arg = int(arg)
        else:
            raise Exception("Не правильный тип входных данных: {}".format(type(arg)))

        data = struct.pack(format_, head, cmd, arg)
        tmp = struct.unpack('<LL', data)
        crc = tmp[0] ^ tmp[1]

        data += struct.pack('<L', crc)
        return data

class BenchModel(QObject):
    data_updated = pyqtSignal(object)
    command_completed = pyqtSignal(object)
    connection_changed = pyqtSignal(bool)
    error_occurred = pyqtSignal(str)
    handle_done = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.worker = BenchWorker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.worker.data_processed.connect(self.data_updated)
        self.worker.command_result.connect(self.command_completed)
        self.worker.error_occurred.connect(self.error_occurred)
        self.worker.done_signal.connect(self.handle_done)

        self.thread.start()

    def connect(self, port, baudrate):
        result = self.worker.connect_serial(port, baudrate)
        self.connection_changed.emit(result)

    def disconnect(self):
        self.worker.disconnect_serial()
        self.connection_changed.emit(False)

    def send_command(self, cmd, arg):
        self.worker.send_command(cmd, arg)

    def execute_sequence(self, commands):
        for cmd, arg in commands:
            self.send_command(cmd, arg)


    def __del__(self):
        self.thread.quit()
        self.thread.wait()