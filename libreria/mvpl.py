"""
mvpl.py

Metis Vela Python Library

29/02/16
Andrea Mastrangelo
"""
import comLib, struct, time
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import numpy as np

NMEA={};
NMEA['MVIC']=[0,1,5,9,13,17]
NMEA[10]=[['b','l','f','f','f','f','f'],[]]#MVIC
NMEA[7]=[['b','l','l','L','L','L','f','f','f','f','f','f','f','b','b','b'],['tipo','lat','lon','gradi','date','times','vel','roll','pitch','yaw','temp','left','right','wspeed','wdir_1','wdir_2']]#MVUP
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

def createDataStorage(tipo):#create index of data storage dictionary
	data={}
	for i in NMEA[tipo][1]:
		data[i]=[]
	data['tipo']=tipo
	return data

def storeData(buff, result):#for every iteration store last income data string in the dict
	i=1
	tipo=result[0]
	while i < len(NMEA[tipo][1]):
		buff[NMEA[tipo][1][i]].append(result[i])
		i=i+1

def plot(data, figure):
	if data[0][0]==7:
		figura=figure['telemetria'][0]
		canvas=figure['telemetria'][1]
		roll, pitch, yaw, time, scarroccio=[],[],[],[],[]
		figura.clf()
		for i in data[-25:]:
			roll.append(i[7])
			pitch.append(i[8])
			yaw.append(i[9])
			time.append(i[5]/1000)
			scarroccio.append(i[9])

		plot_1=figura.add_subplot(211)
		plot_1.plot(time,roll)
		plot_1.plot(time,pitch)
		plot_1.plot(time,yaw)

		plot_2=figura.add_subplot(212)


		canvas.draw()

def saveData(filename, data, strtipo):
	file = open (filename,"w")
	file.write(time.strftime("%d/%m/%y %H:%m:%S"))
	file.write("type="+str(strtipo))
	print data.keys()
	#for i in NMEA[strtipo][1]:
		#if not i=='tipo':
			#file.write(str(i)+": ")
			#file.write(str(data[i]))
			#file.write("\n")
	file.close()

