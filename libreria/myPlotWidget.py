"""
This module defines a Widget (from pyqtgraph.PlotWidget) that plots a curve and
then creates a moving windows that shows a slice of the curve and updates
according to a tick signal.

The curve to be plotted can be any function that takes in input a list of times
in milliseconds and returns the coordinates of the curve in [ x_array, y_array ]
format that will be passed to a pyqtgraph.PlotItem. The returned x_array should
be in seconds (not milliseconds).

The curve function can return the curve evaluated in the milliseconds required,
or in nearby milliseconds, or it can even ignore the arguments
altogether and return the whole curve (this is the preferred functioning, unless
the curve is not known at the beginning or for performance issues).
The Widget will keep track of what has already been plotted and will call the
function again when needed.

Ideally, when the curve function returns the whole curve, it will not make any
further calls.

Conventions:
- The curve function should use only the first and last elements of the time
    interval. In the future the Widget will only pass [ time_min, time_max ].
"""
import pyqtgraph as pg
import numpy as np
import mvpl

# EXAMPLE: curves

# Import the data.
# NOTE: this is used ONLY by the rollCurve function. The widget will
# never-ever-ever use these variables and they should be removed in production.
time, data = mvpl.readDataFile("fileStore/VELA012.TXT")
x_data = np.array(data['time'])
x_data = x_data - x_data[0]#relative time
y_data = np.array(data['roll'])

def rollCurve(x_array,label):
    """Returns the roll values. Ignores the request and send everything altogether."""
    return x_data/1000., y_data

def customCurve(x_array,label):
    """Returns the roll values. Ignores the request and send everything altogether."""
    if label:
        return x_data/1000., np.array(data[label])
    else:
        return x_array/1000., np.sin(x_array*np.pi/period)

def myCurve(x_array,label):
    """ A dummy curve to plot (a sine):
        x_array: array of time values in milliseconds
        Returns:
            [x,y] an array with the coordinates of the points of the curve, time
            in seconds. In case we give an interval outside of the boundary of
            the curve, it can simply return nothing (actually [[],[]]).
    """
    period = 3000
    return x_array/1000., np.sin(x_array*np.pi/period)

# END EXAMPLES

# The Widget. This is production ready.
class myPlotWidget(pg.PlotWidget):
    """Extend the class pyqtgraph.PlotWidget to serve our purposes. If initialized
    it plots a moving window with assigned range and updates the plot at a certain
    framerate given by an external signal.
    Instructions:
     - Pass the parameter initialize=True.
     - Set xHighRange and xLowRange to fix the view range.
     - Overload the method myPlotWidget.Curve to define the data to be plotted.
     - Connect the tickHandler to a tickSignal returning the current time in
        milliseconds.

    TODO: add an argument `datafile` so that when the instance is created it
        loads the data from a specific file, i.e. `fileStore/VELA012.TXT`.
    """
    def __init__(self,*args, **kwargs):
        """Get optional parameters:
            length: length of the media file
            xHighRange: upper semiInterval to be shown, i.e. we will plot
                [ current_time - xLowRange, current_time + xHighRange ]
            xLowRange: as before
            xStartTime: ?
            plotCurve: a function that takes input the required millis and outputs
                the curve in [x_array, y_array] format.
            plotType: TODO planned feature, to tell the widget whether to plot
                everything at the begging or plot as we go or something else.
                Not used right now.
        """
        self.label = kwargs.pop('label',None)
        self.length = kwargs.pop('length',None)
        self.xHighRange = kwargs.pop('xHighRange',2500)
        self.xLowRange = kwargs.pop('xLowRange',2500)
        self.curTime = kwargs.pop('xStartTime',0)
        self.tipology = kwargs.pop('tipology','moving')

        # The curve to be plotted. Simply put a function that takes an interval
        # [xmin, xmax] in milliseconds and returns an array [x,f(x)] with x in
        # seconds and it should work. Fallback function is a sine.
        self.Curve = kwargs.pop('plotCurve',myCurve)

        super(myPlotWidget, self).__init__(*args,**kwargs)

        self.updateMargins(self.curTime)
        self.semiInterval = 2500 # TODO: remove this variable.
        self.xMaxPlotted = None # this variable will keep track of what we've
                                # plotted up to now
        # We get the PlotItem associated in order to modify the plot, e.g
        # add the vertical line in tickHandler.
        self.thisPlotItem = self.getPlotItem()
        self.thisViewBox = self.thisPlotItem.getViewBox()
        if self.tipology == 'static':
            pass
            # TODO: The proper way to avoid the view to move it so add
            # a test in tickHandler.
        else:
            self.vertLine = self.thisPlotItem.addLine(self.curTime/1000.,movable=True)

        # Set the view at the beginning
        self.thisViewBox.setRange(xRange=(self.xmin/1000.,self.xmax/1000.))

        # Initialize the plot if length is defined
        if self.length is not None:
            self.updatePlot(self.length)

    def updateMargins(self, x_center):
        """Sets and update the margins of the view."""
        self.xmin = x_center - self.xLowRange
        self.xmax = x_center + self.xHighRange


    def updatePlot(self, xmax):

        """Update the Plot up to xmax.
        It will only update the x position, graph is entirely plotted at the beginning
        """

        if self.xMaxPlotted is None:
            xstart = self.xmin
        else:
            xstart = self.xMaxPlotted
        if xmax - xstart < 250:
            return None
        interval = range(xstart,xmax,250)

        # Ensures the interval contains xmax
        # FIXME: This code might be useless after a couple of iteration.
        try:
            range_test = interval[-1] < max
        except:
            range_test = False
        if range_test:
            interval.append(xmax)

        interval = np.array(interval)
        x, y = self.Curve(interval, self.label)
        self.plot(x,y)
        self.xMaxPlotted = int(x[-1]*1000)

    def totalTimeChangedHandler(self, newTotalTime):
        self.updatePlot(newTotalTime)

    def tickHandler(self, tick):
        """
        Connect this slot with a phonon.MediaObject.tick signal.
        Handles the tick signal received from a phonon.MediaObject to keep
        the plot in sync with the reproduction.
        """

        # Set the current time to the tick signal received and update the margins
        # of the view and the plot.
        self.curTime = tick
        self.updateMargins(self.curTime)
        self.updatePlot(self.xmax)

        # Move the view according to the new margins and set the vertical line
        # to the current time.
        # TODO: to avoid the moving windows, add a test here:
        #if self.tiplogy == 'moving':
        self.thisViewBox.setRange(xRange=(self.xmin/1000.,self.xmax/1000.))
        self.vertLine.setValue(self.curTime/1000.)

    def staticPlot(self, data):
        """
        Function to plot telemetry data during reception
        Where widget has multiple plot it uses multiple color

        TODO: set labels, title, legends
        """
        self.clear()
        self.addLegend()
        color=[(255,0,0),(0,255,0),(0,0,255),(255,255,255),(200,150,150)]
        if isinstance(self.label,list):#there are more than one data to plot here
            for i in range(len(self.label)):#we need more color
                self.plot(data['times'][-25:],data[self.label[i]][-25:], pen=color[i],name=self.label[i])
        else:
            self.plot(data['times'][-25:],data[self.label][-25:],pen=color[0],name=self.label)
        try:
            self.setXRange(data['times'][-25],data['times'][-1])
        except IndexError:#not yet enough data
            self.setXRange(data['times'][0],data['times'][-1])
