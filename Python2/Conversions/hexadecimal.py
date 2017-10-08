#!python2

import subprocess

def Start():
	print "1. INPUT DECIMAL"
	print "2. INPUT HEXADECIMAL"
	print "3. INPUT BINARY"
	inp = input("INPUT OPTION NO\n> ")
	if inp == 1:
		print '1'
		Decimal()
	elif inp == 2:
		print '2'
		Hexadecimal()
	elif inp == 3:
		print '3'
		Binary()
	elif inp == 0:
		exit(0)
	else:
		Start()

	Start()


#convert to hex
def Decimal():
	data = raw_input("Input a DECIMAL to convert into hex&bin\n> ")
	num = int(data)
	print 'hex', hex(num)
	print 'bin', bin(num)
	subprocess.call("pause", shell = True)

#def Hexadecimal():
#	data = input("Input a HEXADECIMAL to convert to dec&bin")
def Hexadecimal():
	data = raw_input("Input a HEXADECIMAL to convert to dec&bin\n> ")
	try:
		check = data[1]
	except:
		check = 0

	if check == 'x':
		num = int(data, 0)
	else:
		num = int(data, 16)

	print 'DEC', num
	print 'BIN', bin(num)
	subprocess.call("pause", shell = True)

#Binary input
def Binary():
	data = raw_input("Input a BINARY to convert to hex&dec\n> ")
	num = int(data, 2)

	print 'DEC', num
	print 'HEX', hex(num)
	subprocess.call("pause", shell = True)


Start()