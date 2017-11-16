try:
	with open("/media/usb0/LABSD.txt", "r") as f:
		data = f.readlines()
except IOError:
	print('cannot open')
else:
	print(data)
	f.close()