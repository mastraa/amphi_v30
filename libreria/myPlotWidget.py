import pyqtgraph as pg
import numpy as np

class myPlotWidget(pg.PlotWidget):
    """Extend the class pyqtgraph.PlotWidget to serve our purposes.
    TODO: add an argument `datafile` so that when the instance is created it
    loads the data from a specific file, i.e. `fileStore/VELA012.TXT`.
    """
    def __init__(self, *args, **kwargs):
        super(myPlotWidget, self).__init__(*args,**kwargs)
        self.period = 3000
        self.semiInterval = 2500
        # We get the PlotItem associated in order to modify the plot, e.g
        # add the vertical line in tickHandler.
        self.thisPlotItem = self.getPlotItem()

    def tickHandler(self, tick):
        """
        Connect this slot with a phonon.MediaObject.tick signal.
        Handles the tick signal received from a phonon.MediaObject to keep
        the plot in sync with the reproduction.
        """
        x = np.arange(tick - self.semiInterval, tick + self.semiInterval,250)
        y = np.sin(x*np.pi/self.period)
        x = x/1000. #put x in seconds
        self.plot(x,y, clear=True)
        self.thisPlotItem.addLine(x=tick/1000.)
