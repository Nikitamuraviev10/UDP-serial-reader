

class DeviceParametersModel:
    def __init__(self):
        self.time = []
        self.power_voltage = []
        self.power_current = []
        self.signal_voltage = []
        self.signal_current = []
        self.target_angle = []
        self.angle = []
        self.log_file = None

    def update_data(self, key, value):
        if hasattr(self, key):
            array = getattr(self, key)
            array.append(value)

 

    def log_data(self, data):
        if self.log_file is not None:
            self.log_file.write(data)

    def log_enable(self, enable):
        if enable:
            self.log_file = open('log.bin', 'wb')
        else:
            self.log_file.close()
            self.log_file = None
