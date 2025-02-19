# main.py
from PyQt5.QtWidgets import QApplication

from model.bench_model import BenchModel
from view.bench_view import BenchView
from controller.bench_controller import BenchController

from controller.device_parameters_controller import DeviceParametersController
from model.device_parameters_model import DeviceParametersModel
from view.device_parameters_view import PlotWindowView
from  receiver import ReceiverThread

def main():
    app = QApplication([])
    
    # model = BenchModel()
    # view = BenchView()
    # controller = BenchController(model, view)
    
    # view.show()

    # Создаем модель, представление и контроллер
    model = DeviceParametersModel()
    view = PlotWindowView()
    controller = DeviceParametersController(model, view)

    # Настройки для UDP-соединения
    ip = "localhost"  # Замените на нужный IP-адрес
    port = 41000  # Замените на нужный порт

    # Создаем и запускаем поток приема данных
    receiver_thread = ReceiverThread(ip, port, controller)
    receiver_thread.start()

    # Показываем главное окно
    view.show()
    app.exec_()

if __name__ == "__main__":
    main()