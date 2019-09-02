cache = [[0,0,0],
		 [0,0,0],
		 [0,0,0],
		 [0,0,0],
		 [0,0,0],
		 [0,0,0],
		 [0,0,0],
		 [0,0,0]]

# tag, valid, dato
mem = [[7],[0],[0],[8],[0],[0],[0],[1],[0],[0],[0],[5],[0],[9],[0],[0]]
addTemp = 3

def access (mem, cache, add, data):
	tag = getTag(add)
	block = getBlock(add)
	if (cache[block][0]==0 & cache[block][1]==0 & cache[block][2]==0):
		print ("Miss, cold $")
		print (cache)
	elif (cache[block][0]==tag & cache[block][1]==1 & cache[block][2]!=data):
		cache[block][2]=data
		print (cache)
		#Se actualiza este cache se deben invalidar los demas 
	elif ()

def getTag(address):

def getBlock(address):