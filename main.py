# main.py
from PyQt5.QtWidgets import QApplication

from model.bench_model import BenchModel
from view.bench_view import BenchView
from controller.bench_controller import BenchController

def main():
    app = QApplication([])
    
    model = BenchModel()
    view = BenchView()
    controller = BenchController(model, view)
    
    view.show()
    app.exec_()

if __name__ == "__main__":
    main()