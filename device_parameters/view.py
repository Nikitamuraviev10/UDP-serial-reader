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
        self.name = "Realtime Plot"
        self.layout = QtWidgets.QVBoxLayout(self)
        
        #Checkbox init
        checkbox_layout = QtWidgets.QHBoxLayout()
        self.logging_checkbox = QtWidgets.QCheckBox("Logging")

        checkbox_layout.addWidget(self.logging_checkbox)

        #Plot init 
        plot_layout = QtWidgets.QHBoxLayout()
        self.voltage = RealtimePlot("Voltage", (0, 40), "Power", "Signal")
        self.current = RealtimePlot("Current", (0, 10), "Power", "Signal")
        self.angle = RealtimePlot("Angle", (-180, 180), "Real", "Target")
        
        plot_layout.addWidget(self.voltage)
        plot_layout.addWidget(self.current)
        plot_layout.addWidget(self.angle)

        self.layout.addLayout(checkbox_layout)
        self.layout.addLayout(plot_layout)
        
        self.show()

    def show_plot(self, plot, show):
        if show:
            plot.show()
        else:
            plot.hide()