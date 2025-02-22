from datetime import datetime
import os

from sequence_sender.command_registry import CommandRegistry


class DeviceParametersModel:
    def __init__(self):
        self.time: list = []
        self.power_voltage: list = []
        self.power_current: list = []
        self.signal_voltage: list = []
        self.signal_current: list = []
        self.target_angle: list = []
        self.angle: list = []
        self.log_file = None

    def update_data(self, key, value) -> None:
        if hasattr(self, key):
            try:
                array: list = getattr(self, key)
                array.append(value)
                if len(array) > 500:
                    array.pop(0)
            except AttributeError:
                print(f"Attribute {key} not found in DeviceParametersModel")

 

    def log_data(self, data) -> None:
        if self.log_file is not None:
            self.log_file.write(data)

    # @CommandRegistry.register("LogEnable", instance="self")
    def log_enable(self, enable:bool) :
        now = datetime.now()
        name = now.strftime("%Y-%m-%d %H-%M-%S")
        name = f'data/{name}.bin'
        
        if enable:
            os.makedirs(os.path.dirname(name), exist_ok=True)
            self.log_file = open(name, 'wb')
        else:
            if self.log_file is not None:
                self.log_file.close()
                name = self.log_file.name
                self.log_file = None
                return name
                
