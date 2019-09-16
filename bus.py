#############################################################
#	Instituto Tecnologico de Costa Rica						#
#	Computer Engineering									#
#															#
#	Programmer: Daniela Hernandez Alvarado (DaniHdez)		#	
#															#
#	Last update:15/9/2019									# 
#															#
#	Arquitectura de Computadores II							#
#	Professor. Jeferson Gonzalez							#
#															#
#############################################################

import threading
import time
import queue 

sleepMem = 2

#memRequests = []
memRequests = queue.Queue()
responseReads = queue.Queue()


memory = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]

def busMemory (idProcessor, address, action, data):
	global memRequests, responseReads
	#request = [idProcessor, address, act, miss]
	#memRequests.append([idProcessor, address, action, data])
	memRequests.put([idProcessor, address, action, data], False)

	if (action == 'read'):
		return responseReads.get()

	else:
		return True

def controlBus (memRequests, responseReads):
	while True:
		#if (not memRequests.empty()):
		request = memRequests.get() # Se que hay elementos en la cola 
		if (request[2]=='write'):
			memory[request[1]][0] = request[3]
		elif (request[2]=='read'):
			responseReads.put(memory[request[1]][0])
		else:
			responseReads.put('Not found')
		#memRequests.clear()
		print ("\033[;105m"+" MEM: ", memory,"\033[;0m")

		time.sleep(sleepMem)

#controlBus(memRequests)
thread5 = threading.Thread(target = controlBus, args = (memRequests, responseReads, ))
thread5.start()			



