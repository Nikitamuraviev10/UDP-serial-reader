from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

class RealtimePlot(pg.PlotWidget):
    def __init__(self, title, y_range, line1_name, line2_name, parent=None):
        super().__init__(parent)
        
        self.setBackground('w')
        self.setTitle(title)
        self.setLabel('left', 'Value')
        self.setLabel('bottom', 'Time')
        self.setYRange(y_range[0], y_range[1])
        
        self.line1 = self.plot(pen=pg.mkPen(color=(255, 0, 0), width=2), name=line1_name)
        self.line2 = self.plot(pen=pg.mkPen(color=(0, 0, 255), width=2), name=line2_name)

    def update_plot(self, times, data1, data2):
        self.line1.setData(times, data1)
        self.line2.setData(times, data2)

class PlotWindowView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QtWidgets.QHBoxLayout(self)
        
        self.voltage = RealtimePlot("Voltage", (0, 40), "Power", "Signal")
        self.current = RealtimePlot("Current", (0, 10), "Power", "Signal")
        self.angle = RealtimePlot("Angle", (-180, 180), "Real", "Target")
        
        self.layout.addWidget(self.voltage)
        self.layout.addWidget(self.current)
        self.layout.addWidget(self.angle)
        
        self.show()

    def show_plot(self, plot, show):
        if show:
            plot.show()
        else:
            plot.hide()