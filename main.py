# main.py
from PyQt5.QtWidgets import QApplication
import sys

from bench.model import BenchModel
from bench.view import BenchView
from bench.controller import BenchController

from device_parameters.controller import DeviceParametersController
from device_parameters.model import DeviceParametersModel
from device_parameters.view import PlotWindowView
from main.main_window import MainWindow
from  receiver import ReceiverThread


def main():
    app = QApplication(sys.argv)
    
    bench_model = BenchModel()
    bench_view = BenchView()
    bench_controller = BenchController(bench_model, bench_view)

    device_parameters_model = DeviceParametersModel()
    device_parameters_view = PlotWindowView()
    device_parameters_controller = DeviceParametersController(device_parameters_model, device_parameters_view)

    # Настройки для UDP-соединения
    ip = "localhost"  # Замените на нужный IP-адрес
    port = 41000  # Замените на нужный порт

    # Создаем и запускаем поток приема данных
    receiver_thread = ReceiverThread(ip, port, device_parameters_controller)
    receiver_thread.start()

    main_window = MainWindow((bench_view, device_parameters_view))
    

    # Показываем главное окно
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()