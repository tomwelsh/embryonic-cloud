#cell.py

#Atomic node type for the multicellular cloud architecture

import zmq
import os
import time
import threading
import json
import API
import random
import ast

#import mcAPI
FUNCREQTO=5

lock=threading.Lock()

class cell:
	#The cell is the superset object.
	#It consists of a genome, which  executes  applications segments according to the enabled functionality within the interpreter.
	#It also consists of the node, which handles communication between both the external environment (PaaS clients) and
	#other cells within the multi-cellular cloud organism.
	#The cell passess appropriate communications between the node and the genome.
	#Additionally it executes functionality which is typical of the life of the cell such as division and self-checking.


	def __init__(self,motherPort,f,divs,hostPort=None):
		self.maxSubs=3
		self.maxDivisions=int(divs)
		self.divisions=int(divs)
		self.lock=threading.RLock()
		print('cell')
		self.motherPort=motherPort
		print(motherPort)
		#self.check=self.selfCheck()
		self.genome=genome(self)
		self.node=node(hostPort,self,self.genome)
		self.node.startNodePub()
		self.sTime=time.time()

		f=int(f)
		if self.motherPort!='0':
			self.node.nodeSubscribe(self.motherPort) #subscribe to this mother cell

		if int(f) != 0:
			#msg={'pl':f}
			#self.node.orgCapacReq(msg)
			self.genome.maxfunc=int(f)
			#self.node.nodePublish("OCRR",int(f),2)


		self.genome.function=random.randint(1,int(f))
		print("added" + str(self.genome.function))
		for i in range(int(self.maxDivisions)):
			self.divide(f,self.maxDivisions/2)
			print('divide')
			print(int(self.divisions))

		#self.genome=genome()
		#self.node.nodeSubscribe(mother)


	def divide(self,f,divs):
	#divide techniques:
		# system calloka
		# via CM
		#p = subprocess.Popen(['python3', 'blankCell.py', 'localhost:' + str(sel in channelf.node.nodeId)], shell=False, stdout=subprocess.PIPE)
		#out = p.stdout.read()
		#return out
		if self.divisions > 0:
			self.divisions=self.divisions-1
			os.system("python3 blankCell.py %s %d %d  & disown" % (str(self.node.nodeId), f, divs))
			time.sleep(10)
			self.refreshLocalNodes()
			#self.node.publishPeers()
			return 1
		else:
			return 0

	def refreshLocalNodes(self):
		with open('nodes'+str(self.node.pubPort),'r') as nFile:
			for line in nFile.readlines():
				if (line.rstrip('\n') != self.node.nodeId) & (line.rstrip('\n') not in self.node.localNodes):
					self.node.nodeSubscribe(line.rstrip('\n'),True)


	def startCellThread(self,type=None):
		t=threading.Thread(target=self.cellLoop)
		t.daemon = True							#permit ctr+c and the like
		#self.pubThreads.append(t)
		t.start()
		#print "Created Cell Loop"

	def cellLoop(self):
		#this is the main loop
#		self.startSubThread()
#		self.startAPIThread()
					#CELL LOOP
			# 1 - Cell functions:
			#     Send check requests
			#	  Divide requests etc.

			# - Check for keepalives
			#	-if > threshold remove from listna
		self.startSubThread()
		while(1):
			keepAlive=0
			if ((int(time.time()-self.sTime)) % 10) == 0:	#broadcast keepalive
				self.node.sendKA()
				#print(self.node.nodeId + "OKA")
					#print c.node.localNodes

			if ((int(time.time()-self.sTime)) % 15) == 0:				#every minute publish peers
				#print('publish and check')
				self.node.publishPeers()
				#if (len(self.node.localNodes)) < self.node.maxNodes:					#if not many peers, request some
				#		self.node.nodePublish("OPRQ","")
				#check for app requests
				#check for

			if ((int(time.time()-self.sTime)) % 60) == 0:
				self.node.checkTimeouts()

			if ((int(time.time()-self.sTime)) % 10) == 0:
				self.selfOrganise()

		#	if ((int(time.time()-self.sTime)) % 500) == 0:
		#		self.node.clearBadNodes()

			time.sleep(1)

			#check

	def selfOrganise(self):
		local=self.node.getLocalFuncs() #array of all local functions
		#if our function is
		#	-repeated then differentiate
		ch=[]

		#first we differentiate if function is not duplicated or not seen
		try:
			self.lock.acquire()

			if self.genome.function in local:
				poss=1/(local.count(self.genome.function)+1)
				if random.random() < poss:
					#print(self.genome.function)
					for f in range(self.genome.maxfunc): # e.g. [1,2,3,4]
						if f+1 not in local and f+1!=self.genome.function:
							ch.append(f+1)

						if len(ch) >0:
							self.genome.function=random.choice(ch)
							print(local)
							print(ch)

		finally:
			self.lock.release()



	def startSubThread(self,type=None):
		#lock=Lock()
		t=threading.Thread(target=self.subLoop)
		t.daemon = True							#permit ctr+c and the like
		self.node.pubThreads.append(t)
		t.start()
		#print "Created PubLoops"

	def startAPIThread(self,type=None):
		t=threading.Thread(target=self.startRESTAPI)
		t.daemon = True							#permit ctr+c and the like
		#self.pubThreads.append(t)
		t.start()
		#print "Created API Loop"


	def startRESTAPI(self):
		self.node.APIServer=API.eAPI
		self.node.APIServer.addCellRef(self)
		self.node.APIServer.startAPI()



	def startAPILoop(self):
		#!!!depcreated, use startRESTAPI!!!
		#self.API=mcAPI.mcAPI()
		print("API LOOP")
		while True:
			#self.lock.acquire()
			message = self.node.API.recv().decode()
			#print(message)
			self.node.apiHandler(str(message))
			self.node.API.send_string("Echo: " + message)
			#]print("Echo: " + str(message))
			#self.lock.release()


	def subLoop(self):

		while True:
			subs=dict(self.node.poller.poll())		#poll the sockets
		#except KeyboardInterrupt:
			#break
		#	print
			for n in list(self.node.localNodes.keys()):

				#print(n)
				#print(subs)
				if self.node.localNodes[n] in subs:						#if data is recieved
					message =  self.node.localNodes[n].recv_json(zmq.DONTWAIT) 			#recieve data
					self.node.messageHandler(message)
			time.sleep(0.01)





class node:

	#node class using zeromq
	#The node:
	# -  exposes a socket for external clients to communicate with the cloud, passing messages between the client and the cloud
	# - exposes a publication socket for neighbour nodes to subscribe to and recieve messages
	# - subscribes to a set number of neighbours in order to recieve updates from them
	# - examines messages to assess their relevance, processes them if:
	#	- they are global mc messages
	#	- are for their function
	#	- are for their application
	#	- are for their instance
	# - forwards if not relevant but remaining ttl > 1


	def __init__(self,port,cell,genome):

		#!@!@!Messages@!@!@~~


		self.orgMsgs= {
			"OKA" : self.orgKeepAlive,  #keep alive
			"OSRQ" : self.orgStateReq, #State Req
			"OSRR" : self.orgStateResp, #State Req Resp
			"OCRQ" : self.orgCapacReq, #Capacity Request (remote cell may differentiate if possible)
			"OCRR" : self.orgCapacResp, #Capacity Req Respons - we send if we divide or add
			"OPRQ" : self.orgReqPeers, #Request peers
			"OPAR" : self.orgPeerAdv #Peer advertisment
		}

		self.funMsgs= {
			"FDPR": self.funTrafIn,
			"FAOT": self.funTrafOut
		}


		self.apiMsgs= {
			"PFRQ" : self.APIfuncLoadReq,  #application load request
			"PAPP" : self.APIPushApp
		}

		#highly variable performance variables!
		self.maxNodes=4
		self.badThreshold=10
		self.capRespThresh=180
		self.divRespThresh=180
		self.prop=0
		#data structs
		self.pubThreads=[]
		self.localNodes={}							#neighbours struct id:[subscribeSocket,tic]
		self.nodeData={}							#0- timeouts, 1 - selfcheck timeouts, 2 - functions, 3 -Div or not
		self.badNodes={}
		self.capacResp=[{},{}]							#last times since capacity response		 					#last times since division response
		self.localFuncs={} #0 hop
		#print 'node'
		self.ctx = zmq.Context.instance()			#create context - 1 per thread
		self.poller = zmq.Poller()					#poller object is used to loop through multiple sockets
		self.nodeId=port
		#print(genome.apps)
		self.genome=genome
		self.cell=cell
		self.startDebug()
		self.APISock=False

		#print(self.genome.apps)
		#self.api=mcAPI.mcAPI()
		#self.appRequests

	def getLocalFuncs(self):
		t=[]
		self.cell.lock.acquire()
		try:
			for n in list(self.nodeData.keys()):
				t.append(self.nodeData[n][2])
		finally:
			self.cell.lock.release()
		return t



	def startDebug(self):
		self.debug_send=self.ctx.socket(zmq.PUSH)
		self.debug_send.connect('tcp://127.0.0.1:5558')

	def debug(self,typ,msg,ttl=-99):
		self.debug_send.send_json({"id":self.nodeId,"typ":typ,"msg":msg,"ttl":str(ttl)})

	def startAPISock(self):
		self.API = self.ctx.socket(zmq.REP)
		self.API.bind("tcp://*:8000")



	def startNodePub(self,port=None):
		self.nodePub = self.ctx.socket(zmq.PUB) #create new socket for other cells to subscribe to
		if self.nodeId != None:
			self.nodePub.bind("tcp://*:" +str(self.nodeId))
		else:
			p=self.nodePub.bind_to_random_port("tcp://*",min_port=10000,max_port=20000,max_tries=100)		#bind to this port
		self.nodeId='localhost:'+str(p)
		self.pubPort=str(p)
		self.debug("Output","Bound to %s" % self.nodeId)
		if self.cell.motherPort != '0':
			self.informSubscription(self.cell.motherPort.split(":")[1])


	def informSubscription(self,nodeId):
		with open('nodes'+str(nodeId),'a') as nodeF:
			nodeF.write(self.nodeId+"\n")


	def nodeSubscribe(self,nId,div=False):
		feed=random.randint(1,self.maxNodes+self.cell.divisions)
		if div==True:					#if it a child cell
			if(nId != self.nodeId):
				try:
					sock=self.ctx.socket(zmq.SUB) 	#create a new subscribe socket
					sock.connect("tcp://"+nId) 		#subscribe 	to this id
					sock.setsockopt(zmq.SUBSCRIBE, b'')	#subscribe to this feed?
					#sock.setsockopt((zmq.SUBSCRIBE, (str(feed).encode('UTF-8'))))
					self.poller.register(sock, zmq.POLLIN)			#register it on the poll
					self.localNodes[nId]=sock
				#	self.nodeData[nId]=[time.time(),0,0]
					self.nodeData[nId]=[time.time(),0,0,True]
					#print("\n\nSubscribed to node %s" %nId)
					self.debug('out', json.dumps({'typ':'sub','node':nId}))

				except zmq.error.ZMQError:
					print("Incorrect Address")
					return 0
		elif div==False:						#if it is not
			if len(self.localNodes) < self.maxNodes:
				if(nId != self.nodeId):
					try:
						sock=self.ctx.socket(zmq.SUB) 	#create a new subscribe socket
						sock.connect("tcp://"+nId) 		#subscribe 	to this id
						sock.setsockopt(zmq.SUBSCRIBE, b'')	#subscribe to this feed?
					#	sock.setsockopt((zmq.SUBSCRIBE, (str(feed).encode('UTF-8'))))
						self.poller.register(sock, zmq.POLLIN)			#register it on the poll
						self.localNodes[nId]=sock
						self.nodeData[nId]=[0,0,0,False]
						#print("\n\nSubscribed to node %s" %nId)
						self.debug('out', json.dumps({'typ':'sub','node':nId}))

					except zmq.error.ZMQError:
						print("Incorrect Address")
			else:
				return 0


	def nodeUnsubscribe(self,nId):
		self.cell.lock.acquire()

		self.localNodes.pop(nId)
			#self.nodeData.pop(nId)   #keep data
		if self.nodeData[nId][3]==True:
			self.cell.divisions=self.cell.divisions+1
			self.cell.divide(self.genome.maxfunc,self.cell.maxDivisions/2)

		self.cell.lock.release()
		#print(self.nodeData)


	def nodePublish(self,typ,payload,ttl=0):
		#print(msg)
		#ttl=0
		self.nodePub.send_json({'id':self.nodeId,'typ':typ,'pl':payload,'ttl':ttl})
		self.debug('pub', json.dumps({typ:payload}),ttl)


	def messageHandler(self,msg):
		#message structure:
		# SocketNumber:
		#				APP			APPHASH:SEGMENTHASH:INSTANCEHASH:MSGTYPE:MSGPAYLOAD:(TTL)
		#			    ORG 		MSGTYPE:PAYLOAD:(TTL)
		#				FUN
		#
	#	print msgs
		self.debug('recv',json.dumps(msg))
		#print msg
		if msg['typ'][0]=="A":
			self.appMsgs[msg['typ']](msg)
		elif msg['typ'][0]=="O":
			self.orgMsgs[msg['typ']](msg)
		elif  msg['typ'][0]=="F":
			self.funMsgs[msg['typ']](msg)
		elif  msg['typ'][0]=="P":
			self.apiMsgs[msg['typ']](msg)
		else:
			self.debug('out',json.dumps({'typ':'err','msg':msg}))



	def apiHandler(self,msg):
		#new=msg.split(",")
		#print(new)
		self.apiMsgs[msg['typ']](msg)
		#self.apiMsgs[new[0]](new)

	def getKeepAlives(self):
		for n in list(self.nodeData.keys()):
			print((self.nodeData[n][0]))

	def clearBadNodes(self):
		for n in list(self.nodeData.keys()):
			if self.nodeData[n][2] >=3:
				self.nodeData[n]=[0,0,0]

	def checkTimeouts(self):
		self.cell.lock.acquire()
		for n in list(self.localNodes.keys()):
			if self.nodeData[n][0]==0:    #if node has never been seen
				self.nodeData[n][1]=time.time() #set last timeout
				self.nodeData[n][2]+=1
				if self.nodeData[n][2] >= 5:
					self.nodeUnsubscribe(n)
					self.debug('out', json.dumps({'typ':'unseen timeout','node':n}))
					#self.nodeData[n][2]=time.time()


			elif self.nodeData[n][0] > 0:
				timeSince=int(time.time()-self.nodeData[n][0])
			#print(timeSince)
			#print(timeSince)lse
				if timeSince > 60:
					self.nodeData[n][1]=time.time() #set last timeout
					self.nodeData[n][2]+=1
					if self.nodeData[n][2] >= 3:
						self.nodeUnsubscribe(n)
						self.debug('out', json.dumps({'typ':'seen timeout','node':n}))
			else:
				print("error %s" % n)
		self.cell.lock.release()



	def sendKA(self):
		self.cell.lock.acquire()
		self.nodePublish("OKA",str([self.genome.function,[k for k in self.getLocalFuncs()]]))#\,	[k for k in self.capacResp[0]],[k for k in self.capacResp[1]]]),0)
		self.cell.lock.release()
	####Organism MSGs#####



	def orgStateReq(self,msg): #State Req
		#!!!Here there should be a cooldown to prevent flooding attacks!!!
		if self.nodeData[msg[0]][1] == 0:
			self.nodeData[msg[0]][1] == time.time()
		elif time.time()-self.nodeData[msg[0]][1] < 60:
			h=self.selfCheck()
			self.nodePublish("OSRR",str(h))
		else:
			self.badNodeCheck(msg[0])


	def orgStateResp(self,msg): #State Req Resp
		if (msg[1] != self.selfCheck()):
			self.badNodeCheck(msg[0])
#OKA RESUBMIT
	def orgKeepAlive(self,msg):  #keep alive
	#	print 'Keep-Alive from: %s' % msg[0]
		#update

		#local and 1 hop  [[localFuncs][remoteFuncs]]

		#add local functs to 1 hop
		#add remote funcs to 2 hostPort
		self.cell.lock.acquire()
		self.nodeData[msg['id']][0]=time.time() #update node time
		self.nodeData[msg['id']][2]=ast.literal_eval(msg['pl'])[0]
		self.capacResp[0][ast.literal_eval(msg['pl'])[0]]=time.time()
		for f in ast.literal_eval(msg['pl'])[1]:
			self.capacResp[1][int(f)]=time.time()
		self.cell.lock.release()


	def orgCapacReq(self,msg): #Capacity Request from external cell
		#recieved OCRQ + function
		f=int(msg['pl'])

		print("check func")


		print(self.checkFunc(f))
		print(self.capacResp)
		if (f in self.cell.genome.functions):
			#self.nodePublish("OCRR",f,0)
			print("pass because we send OKA")
			pass
		elif self.checkFunc(f) != 0:
			print("pass because it is in our neighbourhood")
			pass
		else:
			#self.nodePublish("OPRQ",'')
			#self.cell.refreshLocalNodes()
			time.sleep(random.randint(1,4)*30)  # wait for other cells
			#print(self.localNodes)
			#print(self.capacResp)
			if (self.checkFunc(f) == 0):
				if self.cell.genome.capacity > 0:
					self.cell.genome.addFunction(f)
					#self.nodePublish("OCRR",str(f),0) don't because oka
				elif self.cell.divide(f) == 1:
					self.capacResp[0][f]=time.time()
					pass
					#self.nodePublish("OCRR",str(f),0)
				#else:
					#self.nodePublish("OCRQ",str(f))


	def orgCapacResp(self,msg): #Capacity Req Response
		print(msg)
		f=int(msg['pl'])
		#self.capacResp[int(msg['pl'])]=time.time()
		#if checkFunc(f)!=:
		#	if time.time()-self.capacResp[int(msg['pl'])] > 20:
		#		if msg['ttl'] > 0:
		#		  essentially aggreage messages if they are the same
		#			self.nodePublish("OCRR",msg['pl'],msg['ttl']-1)
		self.capacResp[0][int(msg['pl'])]=time.time()



	def orgReqPeers(self,msg): #Request peers
		#print 'Peer Request from: %s' % msg[0]
		#msg[0] id msg[1] is OPRQ
		#Some host msg[0] requests Peers
		#Check if we dont have space or are already subscribed:
			#broadcase request+1hop
			#self.node.publish("OPRQ",msg[0])

		self.publishPeers()


	def orgPeerAdv(self,msg): #Peer advertisment
	#	firstly do we want any more peers?
	#	if len(self.localNodes) < self.maxNodes:
	#		for each new node:
	#			are we not already subscribed?
	#				is the node not flagged as bad?
	#					subscribe
		if msg['ttl']==0 :
			if len(self.localNodes) < self.maxNodes:
				for n in msg['pl']:
					if n != self.nodeId:
						if n not in list(self.localNodes.keys()):			#if not currently subscribed
							if (n not in list(self.nodeData.keys())):		#if never seen before at all
								self.nodeSubscribe(n)						#subscribe,
							elif (n in list(self.nodeData.keys())):
								if not self.nodeData[n][2] >=3 :
									self.nodeSubscribe(n)
			#else:
			#	self.nodePublish('OPAR',msg['pl'],1)
		#else:
		#	self.nodePublish('OPAR',msg['pl'],msg['ttl']-1)

	####API MSGs####
	def APIfuncLoadReq(self,msg):  #function capacity request
		#funcs=msg['template'].split(',')
		f=int(msg['func'])
		#for f in funcs:
		if (f == self.genome.function) or (self.checkFunc(f)!=0):
			pass
			#self.capacResp[0][int(f)]=time.time()
		elif (self.genome.addFunction(f) is True):
			#self.nodePublish("OCRR",str(f),0)
			pass
		elif (self.cell.divide(f)) == 1:
			#self.nodePublish("OCRR",str(f),0)
			pass
			#self.capacResp[0][int(f)]=time.time()
		else:
			self.nodePublish("OCRQ",str(f),0)		#request capacity/differentiate
#						self.nodePublish("OCRQ",str(f),0)		#request capacity/differentiate

			#print(self.capacResp)
			#if (int(f) not in self.capacResp) or ((time.time() - self.capacResp[int(f)]) > self.capRespThresh):			#if no response to capacity request
			#	self.nodePublish("OCRQ",str(f),1)

	def APIPushApp(self,data):
		#load the app and data
		#if our function, push data and remaining app
		#if not, push to
		app=json.loads(data['pl'])
		a=app[0]
		d=app[1]
		if a[len(a)-1] == self.genome.function:
			self.genome.process(a,d)
		else:
			self.nodePublish("FDPR",app,0)

	def APIGetApps(self,msg):
		#self.API.send_string("1")96+
		print(self.genome.apps)


	####Function MSGs#####

	def funTrafIn(self,data):
		#app=json.loads(data['pl'])

		a=data['pl'][0]
		d=data['pl'][1]
		if len(a) !=0:
			if a[len(a)-1] == self.genome.function:
				self.genome.process(a,d)
			#else:
			#	if data['ttl']!=1:
			#		self.nodePublish("FDPR",data['pl'],0)
		else:
			self.nodePublish("FAOT",d,0)


	def funTrafOut(self,data):
		print("FOUT: %s " % data['pl'])

###maintenance stuff

	def selfCheck(self):
		#multiple methods of implementation here
		#currently not secure unless backed up TPM
		lines=f.open("cell.py",'rb').read()
		h=SHA256.new()
		h.update(lines)
		return h.hexdigest()

	def checkFunc(self,f):
		f=int(f)
		self.cell.lock.acquire()
		try:
			if f == self.genome.function:
				return 1
			elif (f not in self.capacResp[0]) or (f not in self.capacResp[1]):
				#not found
				return 0
			elif (f in self.capacResp[0]):
				if ((time.time()- self.capacResp[0][f]) > self.capRespThresh):
				#found but timedout
					return 0
				else:
					return 1
			elif (f in self.capacResp[1]):
				if ((time.time()-self.capacResp[1][f]) > self.capRespThresh):

					return 0
				else:

					return 2
		finally:
				self.cell.lock.release()

	def getLocalNodes(self):
		return self.localNodes

	def getSubscribed(self):
		return self.localNodes

	def badNodeCheck(self,n):
		if not self.badNodes[n]:
			self.badNodes[n]=1
		else:
			self.badNodes[n]+=1

		if self.badNodes >= self.badThreshold:
			self.nodeUnsubscribe(n)
			#broadcast message


	def publishPeers(self):
		peers=[]
		for n in list(self.localNodes.keys()):
			peers.append(n)
		if len(peers) > 0:
			self.nodePublish('OPAR',peers,0)		#direct comms only?...........

class genome:
	#the genome manages the execution of application segments

	def __init__(self,cell):
		self.cell=cell
		self.capacity=1
		self.maxfunc=0
		print('genome')
		self.function=0

	#def genomeLoop(self):
		#poll each segment for messages
		#pass messages to segment

	def process(self,app,d):
		d2=d*app.pop()
		if(len(app)>0):
			self.cell.node.nodePublish("FDPR",[app,d2],0)
		else:
			self.cell.node.nodePublish("FAOT",d2,0)

	def addFunction(self,function):
		add=False
		self.cell.lock.acquire()
		if self.capacity > 0:
			self.capacity=self.capacity-1
			self.function=int(function)
			add=True
		else:
			add=False
		self.cell.lock.release()
		return add


	def startInstance(Self,ins):
		os.system("python " + ins)
