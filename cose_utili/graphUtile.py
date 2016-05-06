from PyQt4 import QtCore, QtGui, uic
import pyqtgraph as pg
import sys


class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui=uic.loadUi("esempio.ui")#load gui

		plotter = pg.PlotWidget(name='prova')
		plotter.plot([1,2,3,4,5],[3,7,6,8,9])
		#plotter.clear()
		plotter.plot([1,2,3,4,5],[0.5,3,2,9,1])

		plotter_2=pg.PlotWidget()
		plotter_2.plot([1,2,3,4])

		self.ui.layout.addWidget(plotter)
		self.ui.layout.addWidget(plotter_2)

		self.ui.show() #show gui


app = QtGui.QApplication(sys.argv)
window=MainWindow()
sys.exit(app.exec_())