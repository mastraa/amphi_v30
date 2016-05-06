import pyqtgraph as pg

def qtplotting(widList,data):
	"""
	for every PlotWidget in widList it will plot a graph with correspondant data item
	data list would be like this [x,[y]]
	every item in y list will be plot in correspondant x
	widList and data must be list!!!
	"""
	for i in range (len(widList)):
		print data[i]


plotter = pg.PlotWidget()
pl=[]
pl.append(plotter)
data=[[[1,2,3,4],[[1,2,3,4],[9,8,7,6]]]]

qtplotting(pl,data)


