import pyqtgraph as pg
import numpy as np

def myCurve(x_array):
    """ A dummy curve to plot (a sine):
        x_array: array of time values in milliseconds
    """
    period = 3000
    return np.sin(x*np.pi/period)

class myPlotWidget(pg.PlotWidget):
    """Extend the class pyqtgraph.PlotWidget to serve our purposes.
    TODO: add an argument `datafile` so that when the instance is created it
    loads the data from a specific file, i.e. `fileStore/VELA012.TXT`.
    """
    def __init__(self, *args, **kwargs):
        self.length = kwargs.pop('length',None)
        super(myPlotWidget, self).__init__(*args,**kwargs)
        self.semiInterval = 2500
        # We get the PlotItem associated in order to modify the plot, e.g
        # add the vertical line in tickHandler.
        self.thisPlotItem = self.getPlotItem()
        self.thisViewBox = self.thisPlotItem.getViewBox()
        self.initializePlot()

    def initializePlot(self):
        # if self.length is None:
        #     t_end = 600000
        # else:
        #     t_end = self.length
        t_end = 600000
        x = np.arange(-self.semiInterval, t_end + self.semiInterval,250)
        y = myCurve(x)
        x = x/1000. #put x in seconds
        self.plot(x,y)
        self.thisViewBox.setRange(xRange=(-self.semiInterval/1000.,self.semiInterval/1000.))
        self.vertLine = self.thisPlotItem.addLine(0.,movable=True)

    def tickHandler(self, tick):
        """
        Connect this slot with a phonon.MediaObject.tick signal.
        Handles the tick signal received from a phonon.MediaObject to keep
        the plot in sync with the reproduction.
        """
        xmin = tick - self.semiInterval
        xmax = tick + self.semiInterval
        self.thisViewBox.setRange(xRange=(xmin/1000.,xmax/1000.))
        self.vertLine.setValue(tick/1000.)
