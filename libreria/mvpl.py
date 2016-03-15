"""
mvpl.py

Metis Vela Python Library

29/02/16
Andrea Mastrangelo
"""
import comLib, struct
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import numpy as np

NMEA={};
NMEA['MVIC']=[0,1,5,9,13,17]
NMEA[10]=[['b','l','f','f','f','f','f'],[]]#MVIC
NMEA[7]=[['b','l','l','L','L','L','f','f','f','f','f','f','f','b','b','b'],['tipo','lat','lon','gradi','date','times''vel','roll','pitch','yaw','temp','left','right','wspeed','wdir_1','wdir_2']]#MVUP
NMEA[8]=[['b','l','l','L','L','L','f','f','f','f'],[]]#MVUPC

def decodeNMEA(data):
	val=[]
	byteT=data[0]
	n=0
	for i in NMEA[byteT][0]:
		if i =='b':
			l=1
			val.append(data[n])
		else:
			if i=='i':
				l=2
			else:
				l=4
			array=data[n:n+l]
			while l<4:
				array.append(0)
				l=l+1
			array.reverse()
			val.append(comLib.byteToData(i, array))
			val[-1]=val[-1][0]
			if i == 'f':
				val[-1]=float("%.3f"%val[-1])
		n=n+l
	return val

def plotGraph(data, figura):
	figura.clf()
	x,y = [],[]
	plot_1=figura.add_subplot(211)
	plot_1.plot([1,2,3,4,5],[5,4,3,2,1])

	for i in data[-10:]:
		x.append(i[5])
		y.append(i[1]/1000)
	plot_2=figura.add_subplot(212)
	plot_2.plot(x,y)

	"""self.fig_Inlet.clf()
		ax1f1 = self.fig_Inlet.add_subplot(111)
		ax1f1.plot(np.random.rand(5),np.random.rand(5))
		self.canvasInlet.draw()"""

