import cell
import sys
import threading
import time

if len(sys.argv) < 4:
	print("usage: motherCell.py <motherport> <functions> <divisions> <maxsubs>")


c=cell.cell(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])

def startCellThread():
		#lock=Lock()
	t=threading.Thread(target=c.cellLoop)
	t.daemon = True							#permit ctr+c and the like
	t.start()

c.startCellThread()
c.startAPIThread()
while(1):
	time.sleep(0.1)
