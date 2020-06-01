import zmq
import sqlite3
import time
import threading
import json

import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="emb",
  passwd="emb",
  database="embDebug"
)

class dataServer:



	def __init__(self):
		self.results=[]
		#self.fOut = open('output.txt','w')
				#elf.startCollectThread()


	def resultCollector(self):
		context = zmq.Context()
		results_receiver = context.socket(zmq.PULL)
		results_receiver.bind("tcp://127.0.0.1:5558")
		result = {}
		con = mysql.connector.connect(
		  host="127.0.0.1",
		  user="emb",
		  passwd="emb",
		  database="embDebug"
		)
		while(1):
			result = results_receiver.recv_json()
			cur = con.cursor()
			#print(result)
			try:
				cur.execute("INSERT INTO events (eventTime,eventNode,eventType,eventPayload,eventTTL) \
				VALUES (%s,%s,%s,%s,%s)",(time.time(),result['id'],result['typ'],str(result['msg']),result['ttl']))
				cur.execute("INSERT into nodes (nodeId,nodeLastSeen) VALUES (%s,%s) ON DUPLICATE KEY UPDATE   \
				nodeLastSeen = %s" ,(result['id'],str(time.time()),str(time.time())))
				con.commit()
			except:
				print(result)
		#print("Node successfully added")
			if (result['typ']=='pub'):
				if ('OKA' in result['msg']):
					if result['ttl'] == "0":
						a=json.loads(result['msg'])
						cur.execute("INSERT into nodeFunctions (nodeId,nodeLastSeen,functions) VALUES (%s,%s,%s) \
						ON DUPLICATE KEY UPDATE nodeLastSeen=%s, functions=%s",(result['id'], time.time(), str(result['msg'].split(":")[1]), time.time(), str(result['msg'].split(":")[1])))
						con.commit()
			if (result['typ']=='out'):
				if ('sub' in result['msg']):
					a=json.loads(result['msg'])
					cur.execute(" INSERT IGNORE into nodeSubscriptions (nSId, nodeId,subscribedTo) VALUES (%s, %s,%s)", (result['id']+a['node'],result['id'],a['node']))
					con.commit()
				elif ('timeout' in result['msg']):
					a=json.loads(result['msg'])
					cur.execute("DELETE FROM `nodeSubscriptions` WHERE nSId = %s", (str(result['id']+a['node']),))
					con.commit()
			con.commit()
			msg = "Record successfully added"
				#t=threading.Thread(target=self.messageParse, args=(data,))
				#t.daemon=True
				#t.start()
		con.close()






if __name__ == '__main__':

	d=dataServer()
	d.resultCollector()
	#d.messageParse()
