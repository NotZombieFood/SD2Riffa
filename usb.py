# Importar utilidades
import pyudev

import glib

from pyudev import Context, Monitor

try:
	from pyudev.glib import MonitorObserver

	def device_event(observer, device):
		if (device.action=="add"):
			print ("conectado")
			# Momento de abrir nuestro archivo
			print(device)
		elif (device.action=="remove"):
			print("desconectado")
		else:
			print("error")
except:
	from pyudev.glib import GUDevMonitorObserver as MonitorObserver

	def device_event(observer, action, device):
		if (device.action=="add"):
			print ("conectado")
			# Momento de abrir nuestro archivo
		elif (device.action=="remove"):
			print("desconectado")
		else:
			print("error")

context = Context()
monitor = Monitor.from_netlink(context)

monitor.filter_by(subsystem='usb')
observer = MonitorObserver(monitor)

observer.connect('device-event', device_event)
monitor.start()

glib.MainLoop().run()