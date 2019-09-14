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

import random 
import time
import threading
import bus 
import queue

def genInstruction ():
	instruction = []
	action = random.choice(['read', 'write', 'process'])
	instruction.append(action)

	if (instruction[0]=='read' or instruction[0]=='write'):
		address = random.randint(0, 15)
		instruction.append(address)

	return instruction

requestsQueue = []
#addres, MSI, act
requestsQueue2 = []
requestsQueue3 = []
requestsQueue4 = []


responseQueue = queue.Queue()
responseQueue2 = queue.Queue()
responseQueue3 = queue.Queue()
responseQueue4 = queue.Queue()


def control (idProc, address, estado, act):
	if (idProc == 'CPU1'):
		requestsQueue2.append([address, estado, act])
		requestsQueue3.append([address, estado, act])
		requestsQueue4.append([address, estado, act])
	elif (idProc == 'CPU2'):
		requestsQueue.append([address, estado, act])
		requestsQueue3.append([address, estado, act])
		requestsQueue4.append([address, estado, act])
	elif (idProc == 'CPU3'):
		requestsQueue.append([address, estado, act])
		requestsQueue2.append([address, estado, act])
		requestsQueue4.append([address, estado, act])
	elif (idProc == 'CPU4'):
		requestsQueue.append([address, estado, act])
		requestsQueue2.append([address, estado, act])
		requestsQueue3.append([address, estado, act])
	if (estado == 'search'):
		if (idProc == 'CPU1'):
			responseQ2 = responseQueue2.get()
			responseQ3 = responseQueue3.get()
			responseQ4 = responseQueue4.get()
			if (responseQ2[2] != 'Not found'):
				if (responseQ2[3] == 'M'):
					data = responseQ2[2]
					return data
			if (responseQ3[2] != 'Not found'):
				if (responseQ3[3] == 'M'):
					data = responseQ3[2]
					return data
			if (responseQ4[2] != 'Not found'):
				if (responseQ4[3] == 'M'):
					data = responseQ4[2]
					return data	 
			return ('Not found')
		if (idProc == 'CPU2'):
			responseQ = responseQueue.get()
			responseQ3 = responseQueue3.get()
			responseQ4 = responseQueue4.get()
			if (responseQ[2] != 'Not found'):
				if (responseQ[3] == 'M'):
					data = responseQ[2]
					return data
			if (responseQ3[2] != 'Not found'):
				if (responseQ3[3] == 'M'):
					data = responseQ3[2]
					return data
			if (responseQ4[2] != 'Not found'):
				if (responseQ4[3] == 'M'):
					data = responseQ4[2]
					return data
			return ('Not found')
		if (idProc == 'CPU3'):
			responseQ2 = responseQueue2.get()
			responseQ = responseQueue.get()
			responseQ4 = responseQueue4.get()
			if (responseQ2[2] != 'Not found'):
				if (responseQ2[3] == 'M'):
					data = responseQ2[2]
					return data
			if (responseQ[2] != 'Not found'):
				if (responseQ[3] == 'M'):
					data = responseQ[2]
					return data
			if (responseQ4[2] != 'Not found'):
				if (responseQ4[3] == 'M'):
					data = responseQ4[2]
					return data
			return ('Not found')
		if (idProc == 'CPU4'):
			responseQ2 = responseQueue2.get()
			responseQ = responseQueue.get()
			responseQ3 = responseQueue3.get()
			if (responseQ2[2] != 'Not found'):
				if (responseQ2[3] == 'M'):
					data = responseQ2[2]
					return data
			if (responseQ[2] != 'Not found'):
				if (responseQ[3] == 'M'):
					data = responseQ[2]
					return data
			if (responseQ3[2] != 'Not found'):
				if (responseQ3[3] == 'M'):
					data = responseQ3[2]
					return data
			return ('Not found')
			



def myPrint (idProcessor, message):
	if (idProcessor == 'CPU1'):
		print ("\033[;36m"+" "+idProcessor, message)
	elif (idProcessor == 'CPU2'):
		print ("\033[;35m"+" "+idProcessor, message)
	elif (idProcessor == 'CPU3'):
		print ("\033[;33m"+" "+idProcessor, message)
	elif (idProcessor == 'CPU4'):
		print ("\033[;32m"+" "+idProcessor, message)




def processor(idProc, requestsQueue, responseQueue):
	cache = [[0,'','I'],
			 [0,'','I'],
			 [0,'','I'],
			 [0,'','I'],
			 [0,'','I'],
			 [0,'','I'],
			 [0,'','I'],
			 [0,'','I']]
	myPrint (idProc, cache)
	while(True):
		processorInstruction = [idProc]
		processorInstruction.append(genInstruction())
		myPrint (idProc, processorInstruction)
		time.sleep (0.5)
		if (len(requestsQueue) != 0):
			for request in requestsQueue:
				tag = getTag(request[0])
				block = getBlock(request[0])
				if (request[1] == 'I' or request[1] == 'M' or request[1] == 'S'):
					if (tag == cache[block][0] and cache[block][1] != ''):
						cache[block][2] = request[1]
				else:
					if (tag == cache[block][0] and cache[block][2] == 'M' and request[2] == 'write'):
						myPrint (idProc, 'Accessing memory')
						time.sleep (2)
						bus.busMemory(idProc, request[0], 'write', cache[block][1])
						responseQueue.put([idProc, request[0], cache[block][1], 'M'])
					elif (tag == cache[block][0] and cache[block][1] == 'S' and request[2] == 'write'):
						responseQueue.put([idProc, request[0], cache[block][1], 'S'])
					elif (tag == cache[block][0] and cache[block][1] == 'M' and request[2] == 'read'):
						responseQueue.put([idProc, request[0], cache[block][1], 'M'])
					elif (tag == cache[block][0] and cache[block][1] == 'S' and request[2] == 'read'):
						responseQueue.put([idProc, request[0], cache[block][1], 'S'])
					else:
						responseQueue.put([idProc, request[0], 'Not found', ''])

			requestsQueue.clear()

		if (processorInstruction[1][0] == 'process'):
			time.sleep (0.5)
			myPrint (idProc, 'Processing')
			time.sleep (0.5)

		elif (processorInstruction[1][0] == 'write'):
			address = processorInstruction[1][1]
			tag = getTag(address)
			block = getBlock(address)
			#Arreglar debo buscar primero en otras $'s antes de guardar un dato
			if (cache[block][0]==0 and cache[block][1]=='' and cache[block][2]=='I'):
				myPrint(idProc, 'Miss, cold $')
				#print ('Miss, cold $')
				cache[block][0] = tag
				cache[block][1] = idProc
				cache[block][2] = 'M'
				#Guardar en memoria
				myPrint (idProc, 'Accessing memory')
				time.sleep (2)
				bus.busMemory (idProc, address, 'write', idProc)
				#Si esta en otros $'s Invalidar
				control(idProc, address, 'I', 'write')
				myPrint (idProc, cache)
			elif (cache[block][0]!=tag):
				if (cache[block][2]=='M'):
					myPrint (idProc, 'Miss, coherency')
					#Escribir en memoria el valor de la direccion actual en ese bloque
					wrongAddress = getAddress(cache[block][0], block) 
					tempData = cache[block][1]
					#Escribir en memoria 
					bus.busMemory(idProc, wrongAddress, 'write', tempData)
					cache[block][0] = tag
					cache[block][1] = idProc
					cache[block][2] = 'M'
					#Invalidar el resto de caches en esta direccion
					control(idProc, address, 'I', 'write') 
					myPrint (idProc, cache)
				elif (cache[block][2] == 'S'):
					cache[block][0] = tag
					cache[block][1] = idProc
					cache[block][2] = 'M'
					#Invalidar el resto de caches en esta direccion
					control(idProc, address, 'I', 'write')
					myPrint (idProc, cache)
				elif (cache[block][2] == 'I'):
					cache[block][0] = tag
					cache[block][1] = idProc
					cache[block][2] = 'M'
					#Invalidar el resto de caches en esta direccion
					control(idProc, address, 'I', 'write')
					myPrint (idProc, cache)

			elif (cache[block][0]==tag):
				if(cache[block][2] == 'M'):
					myPrint (idProc, cache)
				elif(cache[block][2] == 'S'):
					cache[block][0] = tag
					cache[block][1] = idProc
					cache[block][2] = 'M'
					control(idProc, address, 'I', 'write')
					myPrint (idProc, cache)
				elif(cache[block][2] == 'I'):
					#Buscar en cache la mas actualizada y guardar en memoria 
					myPrint (idProc, 'Miss, invalid block')
					control (idProc, address, 'search', 'write')
					cache[block][0] = tag
					cache[block][1] = idProc
					cache[block][2] = 'M'
					control(idProc, address, 'I', 'write')
					myPrint (idProc, cache)

		elif (processorInstruction[1][0] == 'read'):
			address = processorInstruction[1][1]
			tag = getTag(address)
			block = getBlock(address)
			if (cache[block][0]==0 and cache[block][1]=='' and cache[block][2]=='I'):
				myPrint (idProc, 'Miss, cold $')
				#Debo traer el dato de memoria y escribirla en $ o de una $ con M
				foundData = control (idProc, address, 'search', 'read')
				if (foundData != 'Not found'):
				#Logica para buscar en memoria si ambas son Not Found no guardar nada y mantener cold $
					cache[block][2] = 'S'
					cache[block][0] = tag
					cache[block][1] = foundData
					#Este else es temporal solo por mientras busco la forma de leer de memoria
				else:
					myPrint(idProc, 'Accessing memory')
					time.sleep(2)
					foundMemData = bus.busMemory(idProc, address, 'read', '')
					if (foundMemData != 0):
						cache[block][2] = 'S'
						cache[block][0] = tag
						cache[block][1] = foundData
					else:
						cache[block][2] = 'I'
						cache[block][0] = tag
						cache[block][1] = ''

				myPrint (idProc, cache)

			elif (cache[block][0]!=tag):
				if (cache[block][2]=='M'):
					myPrint (idProc, 'Miss, coherency')
					tempAddress = getAddress(cache[block][0], block)
					tempData = cache[block][1]
					#Guardar en memoria con tempAddress y tempData
					myPrint (idProc, 'Accessing memory')
					time.sleep (2)
					bus.busMemory(idProc, tempAddress, 'write', tempData)
					#Buscar el dato nuevo en algun $ con M o en memoria
					foundData = control (idProc, address, 'search', 'read')
					if (foundData != 'Not found'):
					#Logica para buscar en memoria si ambas son Not Found no guardar nada y mantener estado anterior
						cache[block][2] = 'S'
						cache[block][0] = tag
						cache[block][1] = foundData
					#Este else es temporal solo por mientras busco la forma de leer de memoria
					else:
						myPrint(idProc, 'Accessing memory')
						time.sleep(2)
						foundMemData = bus.busMemory(idProc, address, 'read', '')
						if (foundMemData != 0):
							cache[block][2] = 'S'
							cache[block][0] = tag
							cache[block][1] = foundData
						else:
							cache[block][2] = 'I'
							cache[block][0] = tag
							cache[block][1] = ''
					myPrint (idProc, cache)
				elif (cache[block][2]=='I'):
					myPrint (idProc, 'Miss, coherency')
					#Buscar el dato nuevo en algun $ con M o en memoria
					foundData = control (idProc, address, 'search', 'read')
					if (foundData != 'Not found'):
					#Logica para buscar en memoria si ambas son Not Found no guardar nada y mantener estado anterior
						cache[block][2] = 'S'
						cache[block][0] = tag
						cache[block][1] = foundData
					#Este else es temporal solo por mientras busco la forma de leer de memoria
					else:
						myPrint(idProc, 'Accessing memory')
						time.sleep(2)
						foundMemData = bus.busMemory(idProc, address, 'read', '')
						if (foundMemData != 0):
							cache[block][2] = 'S'
							cache[block][0] = tag
							cache[block][1] = foundData
						else:
							cache[block][2] = 'I'
							cache[block][0] = tag
							cache[block][1] = ''

					myPrint (idProc, cache)
					#Revisar el protocolo en este caso 
				elif (cache[block][0]=='S'):
					myPrint (idProc, 'Miss, coherency')
					#Buscar el dato nuevo en algun $ con M o en memoria
					foundData = control (idProc, address, 'search', 'read')
					if (foundData != 'Not found'):
					#Logica para buscar en memoria si ambas son Not Found no guardar nada y mantener estado anterior
						cache[block][2] = 'S'
						cache[block][0] = tag
						cache[block][1] = foundData
					#Este else es temporal solo por mientras busco la forma de leer de memoria
					else:
						myPrint(idProc, 'Accessing memory')
						time.sleep(2)
						foundMemData = bus.busMemory(idProc, address, 'read', '')
						if (foundMemData != 0):
							cache[block][2] = 'S'
							cache[block][0] = tag
							cache[block][1] = foundData
						else:
							cache[block][2] = 'I'
							cache[block][0] = tag
							cache[block][1] = ''

					myPrint (idProc, cache)

			elif (cache[block][0]==tag):
				if (cache[block][2]=='M'):
					myPrint (idProc, cache)
				elif (cache[block][2]=='S'):
					myPrint (idProc, cache)
				elif (cache[block][2]=='I'):
					myPrint (idProc, 'Miss, invalid $')
					#Buscar en memoria principal o en cualquier $ con M
					foundData = control (idProc, address, 'search', 'read')
					if (foundData != 'Not found'):
					#Logica para buscar en memoria si ambas son Not Found no guardar nada y mantener estado anterior
						cache[block][2] = 'S'
						cache[block][0] = tag
						cache[block][1] = foundData
					#Este else es temporal solo por mientras busco la forma de leer de memoria
					else:
						myPrint(idProc, 'Accessing memory')
						time.sleep(2)
						foundMemData = bus.busMemory(idProc, address, 'read', '')
						if (foundMemData != 0):
							cache[block][2] = 'S'
							cache[block][0] = tag
							cache[block][1] = foundData
						else:
							cache[block][2] = 'I'
							cache[block][0] = tag
							cache[block][1] = ''

					myPrint (idProc, cache)


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

def getAddress(tag, block):
	block = binary(block, 3)
	tag = bin(tag)
	addressBin = "0b"+tag[2:]+block[2:]
	address = int(addressBin, 2)
	return address


thread1 = threading.Thread(target = processor, args = ('CPU1', requestsQueue, responseQueue, ))
thread1.start()
thread2 = threading.Thread(target = processor, args = ('CPU2', requestsQueue2, responseQueue2, ))
thread2.start()
thread3 = threading.Thread(target = processor, args = ('CPU3', requestsQueue3, responseQueue3, ))
thread3.start()
thread4 = threading.Thread(target = processor, args = ('CPU4', requestsQueue4, responseQueue4, ))
thread4.start()