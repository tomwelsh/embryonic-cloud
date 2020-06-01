#blank cell

import cell
import sys
import threading
import time

c=cell.cell(sys.argv[1],sys.argv[2],sys.argv[3])

def startCellThread():
		#lock=Lock()
	t=threading.Thread(target=c.cellLoop)
	t.daemon = True							#permit ctr+c and the like
	t.start()

c.startCellThread()
while(1):
	time.sleep(0.1)
