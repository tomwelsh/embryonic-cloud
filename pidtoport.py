import zmq
import os
import time
ctx = zmq.Context.instance()
pidRep=ctx.socket(zmq.REP)
pidRep.bind("tcp://127.0.0.1:6666")

while True:
    message = pidRep.recv_json()
    #print(message)


    if message['pid']:
        try:
            b=os.popen('sudo netstat -tlpn | grep %s/python3' % message['pid']).readlines() #anybetter way to do this?
            port=b[0].split(':')[1].split(' ')[0]#
            pidRep.send_json({'pid':message['pid'],'port':port})
            print({'pid':message['pid'],'port':int(port)})
        except Exception as e:
            pidRep.send_json({'pid':message['pid'],'port':-1})
            print(e)



    time.sleep(1)
