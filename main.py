from PyQt5.QtWidgets import QApplication
import sys

from bench.model import BenchModel
from bench.view import BenchView
from bench.controller import BenchController

from device_parameters.controller import DeviceParametersController
from device_parameters.model import DeviceParametersModel
from device_parameters.view import DeviceParametersView

from sequence_sender.command_registry import CommandRegistry
import sequence_sender.command

from sequence_sender.controller import SequenceSenderController
from sequence_sender.view import SequenceSenderView
from sequence_sender.model import SequenceSenderModel


from main.main_window import MainWindow

from  receiver import ReceiverThread

from support.config_parser import ConfigManager
from support.logger_init import setup_logging  



def main():
    app = QApplication(sys.argv)

    config = ConfigManager()

    bench_model = BenchModel()
    bench_view = BenchView()
    bench_controller = BenchController(bench_model, bench_view)

    device_parameters_model = DeviceParametersModel()
    device_parameters_view = DeviceParametersView()
    device_parameters_controller = DeviceParametersController(device_parameters_model, device_parameters_view)

    # Настройки для UDP-соединения
    ip = config.get('Network', 'ip', fallback='localhost')
    port = config.get_int('Network', 'port', fallback=41000)

    # Создаем и запускаем поток приема данных
    receiver_thread = ReceiverThread(ip, port, device_parameters_controller)
    receiver_thread.start()


    # Создаем модуль отправки последовательности
    CommandRegistry.register("LogEnable")(device_parameters_model.log_enable)
    sequence_model = SequenceSenderModel(bench_model, CommandRegistry)
    sequence_view = SequenceSenderView()
    sequence_controller = SequenceSenderController(sequence_model, sequence_view)
    

    # Создаем и показываем главное окно
    main_window = MainWindow((bench_view, sequence_view, device_parameters_view))
    

    # Показываем главное окно
    main_window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    setup_logging()
    main()