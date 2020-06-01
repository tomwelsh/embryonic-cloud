import cell
import sys
import threading
import time

if len(sys.argv) < 4:
	print("usage: motherCell.py <motherport> <functions> <divisions>")


c=cell.cell(sys.argv[1],sys.argv[2],sys.argv[3])

def startCellThread():
		#lock=Lock()
	t=threading.Thread(target=c.cellLoop)
	t.daemon = True							#permit ctr+c and the like
	t.start()

c.startCellThread()
c.startAPIThread()
while(1):
	time.sleep(0.1)
