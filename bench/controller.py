from support.constants import Cmd


class BenchController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Connect signals
        self.view.connect_clicked.connect(self.handle_connect)
        self.view.disconnect_clicked.connect(self.model.disconnect)
        self.view.command_sent.connect(self.handle_command)
        self.view.signal_enable.stateChanged.connect(self.fast_signal_enable_command)

        self.model.data_updated.connect(self.view.log_data)
        self.model.error_occurred.connect(self.view.show_error)
        self.model.connection_changed.connect(self.view.update_connection_state)

    def handle_connect(self, port, baudrate):
        self.model.connect(port, baudrate)

    def handle_command(self, cmd, arg):
        self.model.send_command(cmd, arg)


    def fast_signal_enable_command(self):
        sequence = [
            (Cmd.Clear, 0.0),
            (Cmd.SignalEnable, self.view.signal_enable.isChecked()),
            (Cmd.Start, 0.0)
        ]
        self.model.execute_sequence(sequence)

    def fast_power_enable_command(self):
        sequence = [
            (Cmd.Clear, 0.0),
            (Cmd.PowerEnable, self.view.power_enable.isChecked()),
            (Cmd.Start, 0.0)
        ]
        self.model.execute_sequence(sequence)
