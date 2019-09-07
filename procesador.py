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

import random 
import time
import threading

def genInstruction ():
	instruction = []
	action = random.choice(['read', 'write', 'process'])
	instruction.append(action)

	if (instruction[0]=='read' or instruction[0]=='write'):
		address = random.randint(0, 15)
		instruction.append(address)

	return instruction

requestsQueue = []
#addres, MSI
requestsQueue2 = []
requestsQueue3 = []
requestsQueue4 = []

#def control(todaslascolas, idProc, address, estado)
def control(requestsQueue):
	time.sleep(5)
	requestsQueue.append([1,'M'])
	time.sleep(5)
	requestsQueue.append([2,'M'])
	requestsQueue.append([13,'S'])


def processor(idProc, requestsQueue):
	cache = [[0,'','I'],
			 [0,'','I'],
			 [0,'','I'],
			 [0,'','I'],
			 [0,'','I'],
			 [0,'','I'],
			 [0,'','I'],
			 [0,'','I']]
	print (cache)
	while(True):
		processorInstruction = [idProc]
		processorInstruction.append(genInstruction())
		print (processorInstruction)
		time.sleep (0.5)
		#Recordar verificar que si sea el bloque de cache correcto tag, block 
		if (len(requestsQueue) != 0):
			for request in requestsQueue:
				tag = getTag(request[0])
				block = getBlock(request[0])
				cache[block][2] = request[1]
			requestsQueue.clear()
		print (cache)

		if (processorInstruction[1][0] == 'write1'):
			address = processorInstruction[1][1]
			tag = getTag(address)
			block = getBlock(address)
			if (cache[block][0]==0 and cache[block][1]=='' and cache[block][2]=='I'):
				#print ('Miss, cold $')
				cache[block][0] = tag
				cache[block][1] = idProc
				cache[block][2] = 'M'
				#print (cache)
				#Memoria 
				#Si esta en otros $'s Invalidar
			elif (cache[block][0]!=tag):
				#print ('Miss, coherency')
				#Memoria
				#Si esta en otros $'s con el mismo tag Invalidar
				datoTemp = cache[block][1]
				cache[block][0] = tag
				cache[block][2] = 'M'
				#print (cache)
			#elif (cache[block][0]==tag and cache[block][2]=='M'):
				#Verificar si esta en otro $
				#Invalidar los demas $'s
				#print (cache)
			#elif (cache[block][0]==tag and cache[block][2]=='I'):
				#print ('Miss, invalid $')
				#Debo buscar el $ en el que este 'M'
				#Guardar en memoria 
		#lif (processorInstruction[1][0] == 'read')


def binary(numero, bits):
	numeroTmp = bin(numero)
	numeroTmp = numeroTmp[2:]
	pad = "0"*(bits-len(numeroTmp))
	return "0b"+pad+numeroTmp

def getTag(address):
	#address recibe el siguiente formato '0b1111', el tag es el primer bit 
	address = binary(address, 4)
	tag = int(address[2:3])
	return tag


def getBlock(address):
	#address recibe el siguiente formato '0b1111', el bloque son los ultimos tres bits 
	address = binary(address, 4)
	block = int(address[3:],2)
	return block

thread1 = threading.Thread(target = processor, args = ('CPU1', requestsQueue, ))
thread1.start()
thread2 = threading.Thread(target = processor, args = ('CPU2', requestsQueue2, ))
#thread2.start()
thread3 = threading.Thread(target = processor, args = ('CPU3', requestsQueue3, ))
#thread3.start()
thread4 = threading.Thread(target = processor, args = ('CPU4', requestsQueue4, ))
#thread4.start()
thread5 = threading.Thread(target = control, args = (requestsQueue, ))
thread5.start()