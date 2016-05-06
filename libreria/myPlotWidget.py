import pyqtgraph as pg
import numpy as np

class myPlotWidget(pg.PlotWidget):
    """docstring for myPlotWidget"""
    def __init__(self, *args, **kwargs):
        super(myPlotWidget, self).__init__(*args,**kwargs)
        self.period = 3000
        self.semiInterval = 2500
        self.thisPlotItem = self.getPlotItem()

    def tickHandler(self, tick):
        x = np.arange(tick - self.semiInterval, tick + self.semiInterval,250)
        y = np.sin(x*np.pi/self.period)
        x = x/1000. #put x in seconds
        self.plot(x,y, clear=True)
        self.thisPlotItem.addLine(x=tick/1000.)
