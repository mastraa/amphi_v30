import pyqtgraph as pg
import numpy as np

class myPlotWidget(pg.PlotWidget):
    """docstring for myPlotWidget"""
    def __init__(self, *args, **kwargs):
        super(myPlotWidget, self).__init__(*args,**kwargs)
        self.period = 3000
        self.semiInterval = 2500

    def tickHandler(self, tick):
        x = np.arange(tick - self.semiInterval, tick + self.semiInterval,100) * np.pi / self.period
        y = np.sin(x)
        self.plot(x,y, clear=True)
