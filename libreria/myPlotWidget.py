import pyqtgraph as pg

class myPlotWidget(pg.PlotWidget):
    """docstring for myPlotWidget"""
    def __init__(self, *args, **kwargs):
        super(myPlotWidget, self).__init__(*args,**kwargs)
        self.plot([1,2,3,4],[1,2,3,4])
