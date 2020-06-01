import mysql.connector

class queryNet:



	def getNodes(self):
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
		return result



	def createMYSQLTable(self):
		mydb = conn= mysql.connector.connect(
			host="127.0.0.1",
			user="emb",
			passwd="emb",
			database="embDebug"
			)

		conn= mydb.cursor()
		sql =  "DROP TABLE IF EXISTS nodeSubscriptions"
		conn.execute(sql)
		sql =  "DROP TABLE IF EXISTS events"
		conn.execute(sql)
		sql =  "DROP TABLE IF EXISTS nodes"
		conn.execute(sql)
		sql =  "DROP TABLE IF EXISTS nodeFunctions"
		conn.execute(sql)
		conn.execute('CREATE TABLE events  (eventId int NOT NULL  AUTO_INCREMENT, \
															eventTime REAL, \
															 eventNode VARCHAR(255) , \
															 eventType VARCHAR(255) , \
															 eventPayload VARCHAR(255), \
															 eventTTL VARCHAR(255), \
															 PRIMARY KEY (eventId)) ')

		conn.execute('CREATE TABLE nodes   (nId int NOT NULL AUTO_INCREMENT, \
												nodeId VARCHAR(255) UNIQUE,\
												nodeLastSeen VARCHAR(255), \
												PRIMARY KEY (nId)             )')

		conn.execute('CREATE TABLE nodeFunctions (nFId int NOT NULL  AUTO_INCREMENT, \
															nodeId VARCHAR(255) UNIQUE, \
															nodeLastSeen VARCHAR(255) , \
															functions VARCHAR(255),  \
															PRIMARY KEY (nFId))')


		conn.execute('CREATE TABLE nodeSubscriptions (nSId VARCHAR(255) NOT NULL, \
															nodeId  VARCHAR(255) , \
															subscribedTo VARCHAR(255),\
															FOREIGN KEY (nodeId) REFERENCES nodes(nodeId),\
															FOREIGN KEY (subscribedTo) REFERENCES nodes(nodeId),\
															PRIMARY KEY(nSId)) ')
		#conn.execute('CREATE TABLE nodeSubscriptions (     nSId int NOT NULL AUTO_INCREMENT, \
							#nodeId  VARCHAR(255) , \
							#								subscribedTo VARCHAR(255),\
							#                                FOREIGN KEY (nodeId) REFERENCES nodes(nodeId),\
							#                                FOREIGN KEY (subscribedTo) REFERENCES nodes(nodeId),\
							#                                PRIMARY KEY (nSId)) ')
		conn.close()
