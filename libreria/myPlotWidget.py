import pyqtgraph as pg
import numpy as np

def myCurve(x_array):
    """ A dummy curve to plot (a sine):
        x_array: array of time values in milliseconds
    """
    period = 3000
    return np.sin(x_array*np.pi/period)

class myPlotWidget(pg.PlotWidget):
    """Extend the class pyqtgraph.PlotWidget to serve our purposes.
    TODO: add an argument `datafile` so that when the instance is created it
    loads the data from a specific file, i.e. `fileStore/VELA012.TXT`.
    """
    def __init__(self, *args, **kwargs):
        """Get optional parameters:
            length: length of the media file
            xHighRange: upper semiInterval to be shown, i.e. we will plot
                [ current_time - xLowRange, current_time + xHighRange ]
            xLowRange: as before
            xStartTime: ?
            plotType: TODO planned feature, to tell the widget whether to plot
                everything at the begging or plot as we go or something else.
                Not used right now.
        """
        self.length = kwargs.pop('length',None)
        self.xHighRange = kwargs.pop('xHighRange',2500)
        self.xLowRange = kwargs.pop('xLowRange',2500)
        self.curTime = kwargs.pop('xStartTime',0)
        super(myPlotWidget, self).__init__(*args,**kwargs)

        self.updateMargins(self.curTime)
        self.semiInterval = 2500
        self.xMaxPlotted = None # this variable will keep track of what we've
                                # plotted up to now
        # We get the PlotItem associated in order to modify the plot, e.g
        # add the vertical line in tickHandler.
        self.thisPlotItem = self.getPlotItem()
        self.thisViewBox = self.thisPlotItem.getViewBox()
        self.vertLine = self.thisPlotItem.addLine(self.curTime/1000.,movable=True)

        # Initialize the plot if length is defined
        if self.length is not None:
            self.updatePlot(self.length)

    def updateMargins(self, x_center):
        """Sets and update the margins of the view."""
        self.xmin = x_center - self.xLowRange
        self.xmax = x_center + self.xHighRange

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

    def updatePlot(self, xmax):
        """Update the Plot up to xmax."""
        # FIXME: somehow it doesn't plot a line right after the first plot (when
        # xstart = self.xmin). Try and fix it.
        if self.xMaxPlotted is None:
            xstart = self.xmin
        else:
            xstart = self.xMaxPlotted
        if xstart > xmax:
            return None
        x = np.arange(xstart,xmax,250)
        y = myCurve(x)
        x = x/1000.
        self.plot(x,y)
        self.xMaxPlotted = xmax

    def tickHandler(self, tick):
        """
        Connect this slot with a phonon.MediaObject.tick signal.
        Handles the tick signal received from a phonon.MediaObject to keep
        the plot in sync with the reproduction.
        """
        self.curTime = tick
        self.updateMargins(self.curTime)
        self.updatePlot(self.xmax)
        self.thisViewBox.setRange(xRange=(self.xmin/1000.,self.xmax/1000.))
        self.vertLine.setValue(self.curTime/1000.)
