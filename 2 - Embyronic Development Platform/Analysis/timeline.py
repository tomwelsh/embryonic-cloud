#this script will analyse the events to build a timeline for graph analysis



import time
import mysql.connector
import networkx as nx
import matplotlib.pyplot as plt
import json
import ast
import copy
import matplotlib.pyplot as plt
import sys,os
import csv


class analyseGraph:

	def __init__(self,wd=False):
		self.results=[]
		self.graphHistory=[]
		self.nodes={}
		if wd == False:
			self.wd=("./EmbOut %s" % time.time())
		os.mkdir(self.wd)
		os.chdir(self.wd)
		#f=open("embLog-%s",str(time.time()))
		self.g = nx.DiGraph()


	def getMYSQLResults(self):
		conn= mysql.connector.connect(
		host="127.0.0.1",
		user="emb",
		passwd="emb",
		database="embDebug"
		)
		cursor=conn.cursor()
		cursor.execute('SELECT eventTime, eventNode, eventType, eventPayload,eventTTL from events')
		self.results=cursor.fetchall()
		conn.close()

	def dumpResults(self,r):
		f=open('messages.json','w')
		f2=open('messages.csv','w')
		writer=csv.writer(f2)
		writer.writerows(r)
		f2.close()
		json.dump(r,f)
		f.close()

	def parse(self):
		r2=[]
		start=self.results[0][0]
		for r in self.results:
			r2.append([r[0]-start,r[1],r[2],r[3],r[4]])
		return r2

	def getJSONResults(self):
		f=open('messages','r')
		self.results=json.loads(f.read())
		f.close()


	def newGraph(self):
		g = copy.deepcopy(self.g)
		self.graphHistory.append(g)


	def addNode(self,node):
		newNode=[time.time(),[]]
		self.nodes[node]=newNode
		self.g.add_node(node)

	#def dumpGraphs(self):



	def processMessage(self,row):
		changed=False
		if row[1] not in list(self.nodes.keys()):
			self.addNode(row[1])
			changed=True
		if row[2]=='pub':
			if ('OKA' in row[3]):
				t=str(row[3].split(":")[1])
				#func=ast.literal_eval(t.rstrip("}"))
				func=eval(t.rstrip("}"))
				self.nodes[row[1]][1]=json.loads(func)
				#changed=True

		elif row[2] == 'out':
			msg=json.loads(row[3])
		#    print(msg)
			if (msg['typ']=='sub'):
				if (msg['node'] not in list(self.nodes.keys())):
					self.addNode(msg['node'])
				self.g.add_edge(row[1],msg['node'])
				changed=True
			elif('timeout' in msg['typ']):
				self.g.remove_edge(row[1],msg['node'])
				changed=True
			print(msg)
		return changed

	def processTimeline(self):
		i=0
		for row in self.results:
			result=self.processMessage(row)
			if result==True:
				self.newGraph()
				nx.draw(self.g)
				plt.savefig("graph-%d" % i)
				#plt.show()
				i=i+1
				#    print(row[3])
		print(len(self.graphHistory))

	#    print('OKA')nos
	#    nodes
