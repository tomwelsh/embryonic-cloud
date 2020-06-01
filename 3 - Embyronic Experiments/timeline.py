#this script will analyse the events to build a timeline for graph analysis


from multiprocessing import Pool
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
import numpy
from networkx.readwrite import json_graph


class analyseGraph:

	def __init__(self,d,f,s,wd=False):
		self.results=[]
		self.graphHistory=[]
		self.appHist={}
		self.nodes={}
	#	if wd == False:
		#	self.wd=("./EmbOut %d - %d - %d -  %s" % (d,f,s,time.time()))
		#os.mkdir(self.wd)
		#os.chdir(self.wd)
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
		#f=open('messages.json','w')
		f2=open('messages.csv','w')
		writer=csv.writer(f2)
		writer.writerows(r)
		f2.close()
		#json.dump(r,f)
		#f.close()

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


	def newGraph(self,t):
		self.g.remove_nodes_from(list(nx.isolates(self.g)))
		g = copy.deepcopy(self.g)
		if g is not None:
			self.graphHistory.append([g,t])


	def addNode(self,node):
		newNode=[time.time(),[]]#t.t?
		self.nodes[node]=newNode
		self.g.add_node(node)

	#def dumpGraphs(self):

	def processGraph(self,g):
		#algebraic connectivity

		#spectral gap
		#natural connectivity

		#weighted spectral distribution

		#ac=nx.linalg.algebraicconnectivity.algebraic_connectivity(g.to_undirected())

		if len(g.nodes) > 1:
			try:
				avglust=nx.connectivity.connectivity.average_node_connectivity(g)
			except:
				avglust=-1
			try:			##bug in dataset
				nconn=nx.algorithms.shortest_paths.generic.average_shortest_path_length(g)
			except:
				nconn=-1

			#node degree centrality
			#clustering
			try:
				clust=nx.algorithms.cluster.average_clustering(g)
			except:
				clust=-1
			#closeness
			#try:
			#	close=nx.algorithms.vitality.closeness_vitality(g)
			#except:
			#	close=-1
			#Assortativity - similarity
			try:
				ass=nx.algorithms.assortativity.degree_assortativity_coefficient(g)
			except:
				ass=-1
			#Shortest Paths    /node betweeness
			try:
				spl=nx.algorithms.shortest_paths.generic.average_shortest_path_length(g)
			except:
				spl=-1
			#eccentricity   - longest of shortest paths
			#print('calnetcrit')
			try:
				nc=self.calcNetCrit(g)
			except Exception as e:
				#print(e)
				nc=(-1,-1)
			#print('egr')
			try:
				egr=self.effectiveGraphRes(g)
			except:
				egr=-1
			return (avglust,nconn,clust,ass,spl,nc[0],nc[1],egr)
		else:
			return (-1,-1,-1,-1,-1,-1,-1,-1)


		#network criticality and effective graph resistance for betweeness attacks
		pass

	def calcNetCrit(self,g):
		#also called total resistance distance
		#directed or undirected?
		#...........
		#g2=g.to_undirected()
		a=2/(len(g.nodes())-1)
		lm=nx.linalg.laplacianmatrix.directed_laplacian_matrix(g)
		#lm=nx.linalg.laplacianmatrix.laplacian_matrix(g2)
		l=numpy.linalg.pinv(lm)
		b=a*numpy.trace(l)  #network criticality
		n=b/(len(g.nodes())*(len(g.nodes())-1)) #normalised
	#	print((1/(len(g.nodes())*(len(g.nodes())-1)))*b) #normalised
		#print(n)
		return (b,n)

	def effectiveGraphRes(self,g2):
		##warning undirected
		egr=0
		g=g2.to_undirected()
		ev=nx.linalg.spectrum.laplacian_spectrum(g)
		egr=0
		i=0

		for x in g.nodes():
			for y in g.nodes():
				if x != y:
					egr=egr+(nx.algorithms.distance_measures.resistance_distance(g,x,y))

		c=(len(g.nodes())-1)/egr
		return c

	def processMessage(self,row):
		changed=False
		mtime=float(row[0])
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
			elif ('FDPR' in row[3]):
				s=eval(row[3])
				app=s['FDPR']#
				faot=app[1]
				for x in app[0]:
					faot=faot*x
				#file processing message
				if faot not in list(self.appHist.keys()):
					self.appHist[faot]={'st':mtime,'et':0,'p':1,'o':0,'fpt':mtime,'fot':0,'pr':0,'prt':0}
				else:
					if self.appHist[faot]['fpt']==0:
						self.appHist[faot]['fpt']=mtime
					self.appHist[faot]['p']=self.appHist[faot]['p']+1   #last process time
					if mtime > self.appHist[faot]['et']:
						self.appHist[faot]['et'] = mtime
					if mtime < self.appHist[faot]['st']:
						self.appHist[faot]['st'] = mtime

			elif('FAOT' in row[3]):
				#t=str(row[3].split(":")[1])
				#faot=eval(t.rstrip("}"))
				s=eval(row[3])
				#print(s)
				faot=s['FAOT']#
				#print(faot)
				if faot not in list(self.appHist.keys()):
					self.appHist[faot]={'st':mtime,'et':0,'p':0,'o':1,'fpt':0,'fot':mtime,'pr':0,'prt':0}
				else:
					if self.appHist[faot]['fot']==0:
						self.appHist[faot]['fot']=mtime
					self.appHist[faot]['o']=self.appHist[faot]['o']+1  #last output time
					if mtime > self.appHist[faot]['et']:
						self.appHist[faot]['et'] = mtime
					if mtime < self.appHist[faot]['st']:
						self.appHist[faot]['st'] = mtime

		elif row[2]=='recv':
			#changed=True
			#if any message reltaed to an app is recieved add to the tally
			if (('FDPR' in row[3]) or ('FAOT' in row[3])):
				s=eval(row[3])
				#print(s)
				app=s['pl']
				if type(app) is list:
					faot=app[1]
					for x in app[0]:  #precalculate the end result
						faot=faot*x
				else:
					faot = app
				if faot not in list(self.appHist.keys()):		#if doesnt exist
					self.appHist[faot]={'st':mtime,'et':0,'p':0,'o':0,'fpt':0,'fot':0,'pr':1,'prt':mtime}
				else:
				#	print('update recv %d' % faot)
					if mtime > 	self.appHist[faot]['prt']:			#processreceivetime
						self.appHist[faot]['prt']=mtime
					self.appHist[faot]['pr']=self.appHist[faot]['pr']+1

		elif row[2] == 'out':
			try:
				msg=json.loads(row[3])
		#    print(msg)
				if (msg['typ']=='sub'):
					if (msg['node'] not in list(self.nodes.keys())):
						self.addNode(msg['node'])
					self.g.add_edge(row[1],msg['node'])
					changed=True
				elif('kill' in msg['typ']):
					n=msg['node']
					self.g.remove_node(n)
					print('removed %s' % n)
					changed=True
				elif('timeout' in msg['typ']):
					try:
						self.g.remove_edge(row[1],msg['node'])
						changed=True
					except:
						pass
			except Exception as e:
				print(row)
				print(e)

		return changed

	def mpGraph(self,g):
		data1 = json_graph.node_link_data(g[0])
		s=self.processGraph(g[0])
		t=g[1]-self.results[0][0]
		s2=("%f,%d,%f,%f,%f,%f,%f,%f,%f,%f\n" % (t,len(g[0].nodes()),s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7]))
		return (t,s2,json.dumps(data1))


	def dumpGraphs(self):
		f=open("graphhist","w")
		f2=open("graphstats","w")
		gout=[]
		f2.write("t,N,avgconn,nodeconn,clust,assort,shortpathl,networkcrit,netcritnorm,effegraphres\n")
		i=0

		out=[]
		#(t,s,gout)
		with(Pool(6)) as p:
			for result in p.map(self.mpGraph,self.graphHistory):
				out.append(result)

		out.sort()
		for (t,s,gout) in out:
			f2.write(s)
			json.dump(gout,f)

		#for g in self.graphHistory:
		#	)
		#	s=self.processGraph(g[0])
		#	print(i)
		#	i=i+1
		#
		#	gout.append(json.dumps(data1))
		#print(gout)
		json.dump(gout,f)
		f.close()
		f2.close()

	def dumpAppStats(self):
		f=open("appstats","w")
		f.write("app,toatlprocesstime,shortestprocess,longestrecv,process,output,recv")
		for app in list(self.appHist.keys()):
			a=self.appHist[app]
			ttime=a['et']-a['st']
			spt=a['fot']-a['fpt']
			lr=a['prt']-a['st']
			out=("\n%d,%f,%f,%f,%d,%d,%d" % (app,ttime,spt,lr,a['p'],a['o'],a['pr']))
			f.write(out)
		f.close()


	def processTimeline(self):
		i=0
		for row in self.results:
			result=self.processMessage(row)
			if result==True:
				#print(row)
				self.newGraph(row[0])
				nx.draw(self.g)
				plt.savefig("graph-%d" % i)
				plt.clf()
				#plt.show()
				i=i+1
				#    print(row[3])
		#print(len(self.graphHistory))


	#    print('OKA')nos
	#    nodes
