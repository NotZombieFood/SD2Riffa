#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Proyecto lector SD.

Este script realiza la lectura de dispositivos usb (el cual estará asignado
a usb0, para poder mandarlos a la fpga).

"""

# Importar utilidades

import glib

from pyudev import Context, Monitor

from array import array

import riffa

import time


# Funcion que procesa los datos para mandarlos al fpga
def dataprocess(data):
    """Procesa los datos que recibe del archivo txt."""
    # Array de enteros.
    send_data = array("i")
    # checar cantidad de lineas
    if len(data) > 2:
        print("overflow de lineas")

    # leer primera linea del archivo txt
    if len(data[0]) > 18:
        for x in range(16):
            send_data.append(ord(data[0][x]) + 256)
        print("overflow line0")
    else:
        for x in range(len(data[0]) - 2):
            send_data.append(ord(data[0][x]) + 256)
        for f in range(18 - len(data[0])):
            send_data.append(288)
    send_data.append(192)
    # leer la segunda linea del archivo txt
    if len(data[1]) > 18:
        for y in range(16):
            send_data.append(ord(data[1][y]) + 256)
        print("overflow line1")
    else:
        for y in range(len(data[1]) - 2):
            send_data.append(ord(data[1][y]) + 256)
        for g in range(18 - len(data[1])):
            send_data.append(288)

    print(send_data)
    amt = len(send_data)
    sent = 0
    recibe_data = array.array('I', [0] * amt)
    fd = riffa.fpga_open(0)
    sent = riffa.fpga_send(fd, 0, send_data, amt, 0, True, 0)
    if (sent != 0):
        riffa.fpga_recv(fd, 0, recibe_data, 0)
    riffa.fpga_close(fd)
    print("Data recibida:")
    print(recibe_data)

try:
    from pyudev.glib import MonitorObserver

    def device_event(observer, device):
        """Uno de los dos listeners que tenemos."""
        if (device.action == "add"):
            print("conectado")
            name = device.sys_name
            print(name)
            print(name[len(name) - 4])
            if(name[len(name) - 4] == ":"):
                print("device mala")
            else:
                time.sleep(5)
                try:
                    with open("/media/usb0/LABSD.txt", "r") as f:
                        data = f.readlines()
                except IOError:
                    print('cannot open')
                else:
                    dataprocess(data)
                    f.close()
        elif (device.action == "remove"):
            print("desconectado")
        else:
            print("error")
except:
    from pyudev.glib import GUDevMonitorObserver as MonitorObserver

    def device_event(observer, action, device):
        """Uno de los dos listeners que tenemos."""
        if (device.action == "add"):
            print("conectado")
            name = device.sys_name
            print(name)
            print(name[len(name) - 4])
            if(name[len(name) - 4] == ":"):
                print("Duplicado")
            else:
                time.sleep(5)
                try:
                    with open("/media/usb0/LABSD.txt", "r") as f:
                        data = f.readlines()
                except IOError:
                    print('cannot open')
                else:
                    dataprocess(data)
                    f.close()
        elif (device.action == "remove"):
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
