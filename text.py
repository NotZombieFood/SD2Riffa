try:
	#file:///media/gerardo/LABSD/LABSD.txt
	with open("/media/gerardo/LABSD/LABSD.txt", "r") as f:
		data = f.readlines()
except IOError:
	print('cannot open')
else:
	print(data)
	f.close()