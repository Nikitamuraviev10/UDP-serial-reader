from datetime import datetime
import os


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
            try:
                array: list = getattr(self, key)
                array.append(value)
                if len(array) > 500:
                    array.pop(0)
            except AttributeError:
                print(f"Attribute {key} not found in DeviceParametersModel")

 

    def log_data(self, data):
        if self.log_file is not None:
            self.log_file.write(data)

    def log_enable(self, enable):
        now = datetime.now()
        name = now.strftime("%Y-%m-%d %H-%M-%S")
        name = f'data/{name}.bin'
        
        if enable:
            os.makedirs(os.path.dirname(name), exist_ok=True)
            self.log_file = open(name, 'wb')
        else:
            if self.log_file is not None:
                self.log_file.close()
                self.log_file = None
