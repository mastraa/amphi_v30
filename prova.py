import sys, serial,time
sys.path.append('libreria')
import comLib


ports = comLib.checkSerialDevice()
device = serial.Serial(ports[1],9600)
time.sleep(1)
data = comLib.readIncomeByte(device)
val = comLib.byteToFloat(data[1:5])
print val
device.close()



