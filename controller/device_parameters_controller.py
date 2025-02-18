class DeviceParametersController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_data(self, key, value):
        self.model.update_data(key, value)
        self.update_view()

    def update_view(self):
        self.view.voltage.append_power(self.model.time_val, self.model.power_voltage)
        self.view.current.append_power(self.model.time_val, self.model.power_current)
        self.view.voltage.append_signal(self.model.time_val, self.model.signal_voltage)
        self.view.current.append_signal(self.model.time_val, self.model.signal_current)
        self.view.angle.append_target(self.model.time_val, self.model.target_angle)
        self.view.angle.append_real(self.model.time_val, self.model.angle)

    def log_enable(self, enable):
        self.model.log_enable(enable)

    def log_data(self, data):
        self.model.log_data(data)
