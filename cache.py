#############################################################
#	Instituto Tecnologico de Costa Rica						#
#	Computer Engineering									#
#															#
#	Programmer: Daniela Hernandez Alvarado (DaniHdez)		#	
#															#
#	Last update:6/9/2019									# 
#															#
#	Arquitectura de Computadores II							#
#	Professor. Jeferson Gonzalez							#
#															#
#############################################################

cache = [[0,0,0,'I'],
		 [0,0,0,'I'],
		 [0,0,0,'I'],
		 [0,0,0,'I'],
		 [0,0,0,'I'],
		 [0,0,0,'I'],
		 [0,0,0,'I'],
		 [0,0,0,'I']]

# tag, valid, dato
mem = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]
addTemp = 3

#def access (mem, cache, add, data, act):
def access (mem, cache, add, idPro):
	tag = getTag(add)
	print ('Tag:', tag)
	block = getBlock(add)
	print ('Block:', block)
	if (cache[block][0]==0 & cache[block][1]==0 & cache[block][2]==0):
		print ("Miss, cold $")
		print (cache)
		cache[block][0] = tag
		cache[block][1] = 1
		cache[block][2] = idPro
		memadd = int(add, 2)
		print ('Direccion de memoria', memadd)
		mem[memadd][0] = idPro
		print ('Cache:')
		print (cache)
		print ('Memoria:')
		print (mem)
	#elif (cache[block][0]==tag & cache[block][1]==1 & cache[block][2]!=data):
	#	cache[block][2]=data
	#	print (cache)
		#Se actualiza este cache se deben invalidar los demas 
	#elif ()
	

def getTag(address):
	#address recibe el siguiente formato '0b1111', el tag es el primer bit 
	tag = int(address[2:3])
	return tag

def getBlock(address):
	#address recibe el siguiente formato '0b1111', el bloque son los ultimos tres bits 
	block = int(address[3:],2)
	return block

access (mem, cache, '0b1011', 'CPU1')
