# embryonic-cloud

This repository is for storing the project code for the decentralised embryonic cloud proof-of-concept which was originally developed as part of my phd thesis. 

##Sub projects

It contains the following sub projects:

1) Embryonic Cellular Automata - code for running GUI and ASCII versions of a cellular automata based simulation of the embryonic platform. An additional probabilistic model is included to highlight bounds of the system.

2) Embyronic Development Platform - the embryonic cloud PoC complete with a full stack web application for real-time development and debugging.

3) Embyronic Experiments - a commandline tool for running batches of experiments using the embyronic platform. It provides automated data pre-processing and outputs timelines of network graphs, and structural/performance statistics.


## 1 - Cellular Automata


##Prerequisites

1) Python2
2) Python2-pytk
3) Python2-matplotlib
4) python2-pygubu

##Instructions

Run:
CAExperiment.py for GUI 
caBulkTests.py for batch experimentation, 
caModel.py for probabilistic model


## 2 -  Embyronic Development

##Prerequisites
1) python3
1) python3-zmq
2) python3-flask
3) python3-flask-restful
4) python3-flask-cors
5) python3-mysql.connector
6) mysqld

  mysql -u root
  GRANT ALL PRIVILEGES ON *.* TO 'emb'@'localhost' IDENTIFIED BY 'emb';
  mysql -u emb -p
  CREATE DATABASE embDebug;


##Instructions##

1) Rm events.db
2) createMysqlServer.py
2) Start debugServer.py
4) frontEnd.py
5) firefox http://127.0.0.1:5005/nodes
6)  cellTest.py -> Start API


## 3 - Embyronic Experiments


##Prerequisites
1)python3
2)python3-zmq
3)python3-mysql.connector
4)python3-networkx
5)python3-matplotlib
6)mysql


##Instructions##

1) Check confirugation and then run experiments.py





