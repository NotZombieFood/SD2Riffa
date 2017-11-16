# Importar utilidades
import pyudev

import glib

from pyudev import Context, Monitor

from array import array


# Funcion que procesa los datos para mandarlos al fpga
def dataProccess(data):
	# Array de enteros.
	sendData = array("i")
	sendData.append(1)
	sendData.append(1)
	# checar cantidad de lineas
	if len(data)>2:
		print("overflow de lineas")

	# leer primera linea del archivo txt
	if len(data[0])>18:
		for x in range(16):
			sendData.append(ord(data[0][x])+256)
		print("overflow line0")
	else:
		for x in range(len(data[0])-2):
			sendData.append(ord(data[0][x])+256)
			for f in range(16-len(data[0])-2):
				sendData.append(0)

	# leer la segunda linea del archivo txt
	if len(data[1])>18:
		for y in range(16):
			sendData.append(ord(data[1][y])+256)
		print("overflow line1")
	else:
		for y in range(len(data[1])-2):
			sendData.append(ord(data[1][y])+256)
		for f in range(18-len(data[1])):
			sendData.append(32)
	print(sendData)
	print(len(sendData))
try:
	from pyudev.glib import MonitorObserver

	def device_event(observer, device):
		if (device.action=="add"):
			print ("conectado")
			name = device.sys_name
			print(name)
			print(name[len(name)-4])
			if(name[len(name)-4] == ":"):
				print("device mala")
			else:
				try:
				    with open("/media/gerardo/LABSD/LABSD.txt", "r") as f:
						data = f.readlines()
				except IOError:
				    print('cannot open')
				else:
				  	dataProccess(data)
					f.close()
		elif (device.action=="remove"):
			print("desconectado")
		else:
			print("error")
except:
	from pyudev.glib import GUDevMonitorObserver as MonitorObserver

	def device_event(observer, action, device):
		if (device.action=="add"):
			print ("conectado")
			name = device.sys_name
			print(name)
			print(name[len(name)-4])
			if(name[len(name)-4] == ":"):
				print("device mala")
			else:
				try:
				    with open("/media/gerardo/LABSD/LABSD.txt", "r") as f:
						data = f.readlines()
				except IOError:
				    print('cannot open')
				else:
				  	dataProccess(data)
					f.close()
		elif (device.action=="remove"):
			print("desconectado")
		else:
			print("error")

# Listener de usb 
context = Context()
monitor = Monitor.from_netlink(context)

monitor.filter_by(subsystem='usb')
observer = MonitorObserver(monitor)

observer.connect('device-event', device_event)
monitor.start()

# loop
glib.MainLoop().run()