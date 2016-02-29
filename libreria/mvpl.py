"""
mvpl.py

Metis Vela Python Library

29/02/16
Andrea Mastrangelo
"""
import comLib

NMEA={};
NMEA['MVIC']=[0,1,5,9,13,17]
NMEA[10]=[1,5,9,13,17]


def decodeNMEA(data):
    val=[]
    byteT=data[0]
    data=comLib.splitIncomeData(data,NMEA[byteT])
    if byteT==10:
        for i in data:
            val.append(comLib.byteToFloat(i))
    return val