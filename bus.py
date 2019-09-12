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

import threading

#a = procesador.getAddress (1, 4)
#print (a)

memRequests = []

memory = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]

def busMemory (idProcessor, address, action, data):
#request = [idProcessor, address, act, miss]
	memRequests.append([idProcessor, address, action, data])


def controlBus (memRequests):
	while True:
		if (len(memRequests) != 0):
			for request in memRequests:
				if (request[2]=='write'):
					memory[request[1]][0] = request[3]
					print (memory)
				elif (request[2]=='read'):
					print (memory[request[1]][0])
					#tempMemData = memory[address]
					#Debo pasarlo de alguna forma al cache
			memRequests.clear()
			print ("\033[;31m"+" ", memory)


#controlBus(memRequests)
thread5 = threading.Thread(target = controlBus, args = (memRequests, ))
thread5.start()			



