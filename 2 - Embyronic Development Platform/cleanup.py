#cleanup

import os

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
a=os.popen('ps aux | grep frontEnd.py').readlines()
for l in a:
	if l.find("grep") == -1:
		pid=l.split()[1]
		k="kill %s" % pid
		print(k)
		os.system("kill " + pid)


os.system("rm nodes*")
