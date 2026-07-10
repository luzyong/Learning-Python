from pycomm3 import LogixDriver
with LogixDriver('192.168.1.9') as plc:
	print(plc)
