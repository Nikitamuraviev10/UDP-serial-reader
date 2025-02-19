class DeviceParametersController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_data(self, key, value):
        self.model.update_data(key, value)
        

    def update_view(self):
        self.view.voltage.update_plot(self.model.time, self.model.power_voltage, self.model.signal_voltage)
        self.view.current.update_plot(self.model.time, self.model.power_current, self.model.signal_current)
        self.view.angle.update_plot(self.model.time, self.model.angle, self.model.target_angle)

    def log_enable(self, enable):
        self.model.log_enable(enable)

    def log_data(self, data):
        self.model.log_data(data)
