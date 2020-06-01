 #test cell com
#this file is used for developing and testing cell functionality
#eventually this code will be integrated into the main cell class such that it will be managed in an autonomous fashion


# 1 - spawn spell on designated port
# 2 - subscribe to a mother cell
# 3 - publish messages

import sys
import time
import os
import threading


import cell


c=cell.cell(sys.argv[1],sys.argv[2]) # start cell and bind
    #loop through threads we are subscribed too
c.startCellThread()
ch=0
while ch!=str(99):

#c.node.startAPIThread()
				#loop to prevent main thread from terminating other threads
		#c.lock.acquire()
	print("\n\n\tNode Experimentation menu")
	print("\tNode Id: %s" % c.node.nodeId)
	print("\tLocal Nodes: ")
	for n in c.node.getLocalNodes():
		print("\t %s" % n)
	print(c.node.capacResp)


	print('Options:\n1) Divide\n2)Subscribe\n3)Refresh\n4)Remove Nodes\n5)Send Raw Message\n6)Keep Alives\n7)Publish Peers\n8)SubFromList\n9)StartAPI\n99)Exit')
	ch=input("Selection>")

	if ch=='1':
		print('Dividing\n\n\n')
		print(c.divide())
	elif ch=='2':
		print('Subscribe\n')
		sub=input("Address: ")
		c.node.nodeSubscribe(sub)
	elif ch=='3':
		print('Refreshing\n\n\n')
	elif ch=='4':
		print('Removing nodes\n\n\n')
	elif ch=='5':
		sub=input("Message to Send:")
	elif ch=='6':
		c.node.getKeepAlives()
	elif ch=='7':
		c.node.publishPeers()
	elif ch=='8':
		c.refreshLocalNodes()
	elif ch=='9':
		c.startAPIThread()
	elif ch=='99':
		a=os.popen('ps aux | grep blankCell.py').readlines()
		for l in a:
			if l.find("grep") == -1:
				pid=l.split()[1]
				k="kill %s" % pid
				print(k)
				os.system("kill " + pid)

		open("nodes", "w").close()
		print('Exiting')

	#c.lock.release()

		#poll genome messages
	#	process genome messagess
