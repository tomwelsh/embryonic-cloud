#debug server

import time
import zmq
import pprint
from flask import Flask, render_template
from flask_cors import CORS
import threading
#'import sqlite3
import json

import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="emb",
  passwd="emb",
  database="embDebug"
)


#result_collector()


app = Flask(__name__)
CORS(app) #CSRF VULNERABILITY DONT MAKE PUBLIC

def readData():
	fIn=open('/modules/output.txt')
	line=fIn.readline()
	fIn.close()
	return line

@app.route('/')
def hello_world():
	return "Hello World"

@app.route('/events')
def displayEvents():
	#  print(readData())
	return render_template('listEvents.html')

@app.route('/events2')
def displayEvents2():
    	#  print(readData())etAllEvents
	return render_template('listEvents2.html')

@app.route('/nodes')
def nodeInfo():
	#  print(readData())
	return render_template('nodeInfo.html')

@app.route('/network')
def showNet():
	return render_template('networkStruct.html')


@app.route('/getAllEvents')
def getEvents():
	conn= mysql.connector.connect(
	  host="127.0.0.1",
	  user="emb",
	  passwd="emb",
	  database="embDebug"
	)
	cursor=conn.cursor()
	cursor.execute('SELECT eventTime, eventNode, eventType, eventPayload,eventTTL from events')
	result=cursor.fetchall()
	conn.close()
	return ("{\"data\": %s}" % json.dumps(result))
	#rows=cursor.fetchall()
	#for row in rows:
		#print(row)

@app.route('/getNodes')
def getNodes():
	conn= mysql.connector.connect(
	  host="127.0.0.1",
	  user="emb",
	  passwd="emb",
	  database="embDebug"
	)
	cursor=conn.cursor()
	cursor.execute('SELECT nodeId, nodeLastSeen from nodes')
	result=cursor.fetchall()
	conn.close()
	return ("{\"data\": %s}" % json.dumps(result))

@app.route('/getSubs')
def getSubs():
	conn= mysql.connector.connect(
	  host="127.0.0.1",
	  user="emb",
	  passwd="emb",
	  database="embDebug"
	)
	cursor=conn.cursor()
	cursor.execute('SELECT nodeId, subscribedTo from nodeSubscriptions')
	result=cursor.fetchall()
	conn.close()

	return ("{\"data\": %s}" % json.dumps(result))

@app.route('/getSubs/<nId>')
def getSubsNid(nId):
	conn= mysql.connector.connect(
	  host="127.0.0.1",
	  user="emb",
	  passwd="emb",
	  database="embDebug"
	)
	cursor=conn.cursor()
	cursor.execute('SELECT subscribedTo from nodeSubscriptions WHERE nodeId = %s' % nId)
	result=cursor.fetchall()
	conn.close()

	return ("{\"data\": %s}" % json.dumps(result))


@app.route('/getNetwork')
def getNet():
	data="{ "#\"comment\": \"networkGraph\", "
	  #edges: [{"source":}]
	#}
	conn= mysql.connector.connect(
	  host="127.0.0.1",
	  user="emb",
	  passwd="emb",
	  database="embDebug"
	)
	cursor=conn.cursor()
	cursor.execute('SELECT nodes.nodeId, nodes.nodeLastSeen, nodeFunctions.functions from nodes LEFT JOIN nodeFunctions on nodeFunctions.nodeId = nodes.nodeId')
	result=cursor.fetchall()
	nodes="\"nodes\": [ "
	print(result)
	for r in result:
		nodes=nodes+("{ \"id\": \"%s\", \"caption\" : %f , \"function\" :  %s, "  % (r[0],time.time()-float(r[1]),r[2]))

	cursor.execute('SELECT nodeId, subscribedTo from nodeSubscriptions')
	result=cursor.fetchall()
	edges=" ], \"edges\": [ "
	i=0

	for r in result:
		edges=edges+("{ \"source\" : \"%s\",\"target\" : \"%s\" }, " % (r[0],r[1]))
		i+=1
	conn.close()

	return data+nodes.rstrip(', ')+edges.rstrip(', ')+" ] }"


@app.route('/getNodeFunctions')
def getNodeFuncs():
	data="{ "
	conn= mysql.connector.connect(
	  host="127.0.0.1",
	  user="emb",
	  passwd="emb",
	  database="embDebug"
	)
	cursor=conn.cursor()
	cursor.execute('SELECT nodeId, nodeLastSeen, functions from nodeFunctions')
	result=cursor.fetchall()
	nodes="\"nodeFunctions\": [ "
	for r in result:
		nodes=nodes+("{ \"id\": \"%s\", \"caption\": %f \"functions:\": %s }, "  % (r[0],time.time()-float(r[1]),r[2]))
	conn.close()




	return (nodes.rstrip(', ') + " ] }")


@app.route('/testData')
def testData():
	return render_template('messages.json')




if __name__ == '__main__':
	app.run(port=5005)
