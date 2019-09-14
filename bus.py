#############################################################
#	Instituto Tecnologico de Costa Rica						#
#	Computer Engineering									#
#															#
#	Programmer: Daniela Hernandez Alvarado (DaniHdez)		#	
#															#
#	Last update:14/9/2019									# 
#															#
#	Arquitectura de Computadores II							#
#	Professor. Jeferson Gonzalez							#
#															#
#############################################################

import threading
import time
import queue 

memRequests = []
responseReads = queue.Queue()


memory = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]

def busMemory (idProcessor, address, action, data):
	#request = [idProcessor, address, act, miss]
	memRequests.append([idProcessor, address, action, data])
	if (action == 'read'):
		readData = responseReads.get()
		return readData




def controlBus (memRequests):
	while True:
		if (len(memRequests) != 0):
			for request in memRequests:
				if (request[2]=='write'):
					memory[request[1]][0] = request[3]
				elif (request[2]=='read'):
					responseReads.put(memory[request[1]][0])
			memRequests.clear()
			print ("\033[;31m"+" ", memory)

#controlBus(memRequests)
thread5 = threading.Thread(target = controlBus, args = (memRequests, ))
thread5.start()			



