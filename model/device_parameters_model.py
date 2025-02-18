

class DeviceParametersModel:
    def __init__(self):
        self.time_val = None
        self.power_voltage = None
        self.power_current = None
        self.signal_voltage = None
        self.signal_current = None
        self.target_angle = None
        self.angle = None
        self.log_file = None

    def update_data(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)

    def log_data(self, data):
        if self.log_file is not None:
            self.log_file.write(data)

    def log_enable(self, enable):
        if enable:
            self.log_file = open('log.bin', 'wb')
        else:
            self.log_file.close()
            self.log_file = None
