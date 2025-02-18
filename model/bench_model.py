from PyQt5.QtCore import QObject, pyqtSignal, QThread, QMutex, QMutexLocker
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import struct
from enum import Enum

class Cmd(Enum):
    Pop 		= 0
    Clear 		= 1
    Start 		= 2
    Pause 		= 3
    Reset 		= 4
    StopData 	= 5
    StartData 	= 6
    ResetTime	= 7
    To485 		= 8
    SetMaxAngle = 9
    SetOutut	= 10
    ResetAngle  = 11
    SetMaxPwm   = 12
    SetMinPwm   = 13
    # To push
    SetAngle 	= 1024
    Wait 		= 1025
    FreqResp    = 1026
    PowerEnable = 1027
    SignalEnable = 1028
    # Get
    GetMaxAngle = 2048

class Status(Enum):
    Ok				= 0
    InvalidHead		= 1
    InvalidCrc		= 2
    IsFull			= 3
    Done            = 4

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

    def process_packet(self, status):
        if status[1] == Status.Done:
            self.done_signal.emit()
        self.data_processed.emit(status)

    def send_command(self, cmd, arg):
        response = None
        try:
            data = self.serialize(cmd, arg)
            with QMutexLocker(self.mutex):
                self.serial.write(data)
                self.serial.waitForBytesWritten(500)
        except Exception as e:
            self.error_occurred.emit(str(e))


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

    def handle_done(self):
        # Обработка завершения операции
        pass

    def __del__(self):
        self.thread.quit()
        self.thread.wait()