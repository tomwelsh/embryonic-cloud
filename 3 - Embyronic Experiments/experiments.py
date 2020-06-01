import mysql.connector
import debugServer
import apiClient
import timeline
import time
import queryNetwork
import threading
import os
import json
import random
import zmq
#This script will:

#run batches of experiments
	#store:
		#-all network mesages
		#   -parse for bandwidth / efficiency?
		#   -parse for time
		#   -parse for network structure at each timestep
		#   -   network


#threads.....
#1 - debug server




def cleanUP():
	a=os.popen('ps aux | grep Cell.py').readlines()
	for l in a:
		if l.find("grep") == -1:
			pid=l.split()[1]
			k="kill %s" % pid
			print(k)
			os.system("kill " + pid)
	a=os.popen('ps aux | grep debugServer.py').readlines()
	for l in a:
		if l.find("grep") == -1:
			pid=l.split()[1]
			k="kill %s" % pid
			print(k)
			os.system("kill " + pid)
	#os.system("rm nodes*")

def debug(t,msg):
	print("[%f] - %s\n" % (t,msg) )


ctx = zmq.Context.instance()
debug_send=ctx.socket(zmq.PUSH)
pidReq=ctx.socket(zmq.REQ)

try:
	pidReq.connect("tcp://127.0.0.1:6666")
except:
	print("Can't connect to pid server")
	exit()
wd=False
#if wd == False:
#	wd=("./EmbOut %s" % time.time())
#	os.mkdir(wd)
#	os.chdir(wd)

##########independent variables
divs = 2    #division depth   == size
funcs = 2	#number of functions
subs=3
frate=0.01 #failure rate
ttl=0
badThresh=10
badchances=1
#######################
t=time.time()
debug(time.time()-t, "Starting Tests")
times=1
for i in range(times):
	for funcs in range(2,3):
		for divs in range(6,7):
			for subs in range(6,7):
				try:
					debug(time.time()-t, ("Test - D:%d F:%d S%d FR%f T:%d,%d" % (divs,funcs,subs,frate,badThresh,badchances)))

			#\		os.mkdir("f%d" % x)
			#		os.chdir("f%d" % x)

					qn=queryNetwork.queryNet()
					qn.createMYSQLTable()			#refresh the local table (? should this be a new table everytime?)
					os.system("rm nodes*")
					os.system("python3 debugServer.py & ")
					debug(time.time()-t, " Started Debug Server")
					####### MOTHER CELL #####################
					debug_send.connect('tcp://127.0.0.1:5558')
					os.system("python3 motherCell.py 0 %d %d %d %d %d & " % (funcs,divs,subs,badThresh,badchances))
					debug(time.time()-t, " Spawned Mother Cell")
					client = apiClient.APIClient("127.0.0.1",5000)

					#########################################
					###### LOOP #############################
					# Traffic IN
					# Failures

					#exit_condition =:
					#	totalTime
					#	allNodesFailed
					#	objective
					data=2
					app=[x+1  for x in range(funcs)]
					sTime=time.time()
					while (time.time()-sTime < 1800):

						#if frate > 0:
							#r=random.random(0,)
				#		print(qn.getNodes())
						if (int(time.time() - sTime)) % 10 == 0:
							try:
								client.pushApp(json.dumps([app,data]))
								data=data+1
							except:
								#print('not active')
								pass
						if frate != 0:
							if (int(time.time() - sTime)) % 2 == 0:
								a=os.popen('ps aux | grep blankCell.py').readlines()
								for l in a:
									i=random.random()
									if l.find("grep") == -1:
										if i < frate:
											pid=l.split()[1]
										#	b=os.popen('sudo netstat -tlpn | grep %s/' % pid).readlines() #anybetter way to do this?
										#	port=b[0].split(':')[1].split(' ')[0]#
											pidReq.send_json({'pid':pid})
											m=pidReq.recv_json()
											port=m['port']
											if port !=-1:
												k=("kill %s" % pid)
												debug(time.time(),("killed pid %s-localhost:%s" % (pid,port)))
												nk=("localhost:%s" % port)
												debug_send.send_json({"id":"exp","typ":'out',"msg":json.dumps({'typ':'kill','node': nk}),"ttl":str(99)})

												os.system("kill " + pid)

						time.sleep(1)


					##### END LOOP ##########################
					##### DATA PREPROCESSING ################
					cleanUP()
					wd=("./EmbOut %d - %d - %d - %f -  %s" % (divs,funcs,subs,frate,time.time()))
					os.mkdir(wd)
					os.chdir(wd)
					a=timeline.analyseGraph(divs,funcs,subs)
					a.getMYSQLResults()
					a.dumpResults(a.parse())
					debug(time.time()-t, "Processing Timeline")
					a.processTimeline()
					debug(time.time()-t, "Dumping App Stats")
					a.dumpAppStats()
					debug(time.time()-t, "Dumping Graphs")
					a.dumpGraphs()

					debug(time.time()-t, "Clean Finish")

					##########################################
			#		os.chdir('../')
				finally:
					debug(time.time()-t, "Cleaning Up")
					cleanUP()
					os.chdir("../")


	#########################################
