"""
comLib.py v1.
communication library
libreria comunicazione seriale

Andrea Mastrangelo
28/02/16

"""

import sys, glob, serial
import struct

def checkSerialDevice():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    if sys.platform.startswith('darwin'):
        result = result[1:] #first one is bluetooth device
    return result

def readIncomeByte(device, starter = '$', ender = '*'):
    data=[]
    _xor=0
    if device.inWaiting():#if any data incoming
        if device.read()==starter:
            #print 'starter'
            c=device.read()
            while c!=ender:
                data.append(ord(c))
                _xor=_xor^data[-1]
                c=device.read()
            if _xor==ord(device.read()):
                device.read()#clean \n byte
                return data
            else:
                return 2 #checksum error
        else:
            return 1 #no starter
    else:
        return 0 #no data

def sendByte(device, array, starter = '$', ender = '*'):
    _xor = 0
    device.write(starter)
    for i in array:
        device.write(chr(i))
    device.write(ender)
    device.write(chr(_xor))
    device.write('\n')

def byteToFloat(array):#convert four bytes array to a float value
    array.reverse()
    b = ''.join(chr(i) for i in array)
    return struct.unpack('>f', b)

def byteToData(f,array):#convert four bytes array to a variable typed by f
    b = ''.join(chr(i) for i in array)
    return struct.unpack('>'+f, b)

def splitIncomeData(data, init):
    result=[]
    i=0
    while i<len(init)-1:
        result.append(data[init[i]:init[i+1]])
        i=i+1
    result.append(data[init[i]:])
    return result

def readUntil(device, flag):
    c=0
    while not c==flag:
        if device.inWaiting():
            c=device.read()