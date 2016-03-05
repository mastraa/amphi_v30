"""
mvpl.py

Metis Vela Python Library

29/02/16
Andrea Mastrangelo
"""
import comLib, struct

NMEA={};
NMEA['MVIC']=[0,1,5,9,13,17]
NMEA[10]=['b','l','f','f','f','f','f']#MVIC
NMEA[7]=['b','l','l','L','L','L','f','f','f','f','f','f','f','b','b','b']#MVUP
NMEA[8]=['b','l','l','L','L','L','f','f','f','f']#MVUPC

def decodeNMEA(data):
	val=[]
	byteT=data[0]
	n=0
	for i in NMEA[byteT]:
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