#Python API Client for embroynic PaaS

import requests
import time


class APIClient:


    def __init__(self,address,port):
        self.address=address
        self.port=port


    def checkAPI(self):
        r = requests.get("http://%s:%d/" % (self.address,self.port))
        return r

    def appCapacityRequest(self,app):
        for f in app:
            r=funcCapacityReq(f)

    def checkAppRequest(self,app,timeout):
        responses={} #[] 0-requested, 1 -found
        for f in app:
            responses[f]=self.funcRespCheck(f).text
            if 'not found' in responses[f]:
                responses[f]=self.funcCapacityReq(f).text
        start=time.time()
        while time.time()-start < timeout:
            found=0
            for f in app:
                responses[f]=self.funcRespCheck(f).text
                print(responses[f])
                if 'found' in responses[f]:
                    found+=1
            if found==len(app):
                break
            print(responses)
        print(time.time()-start)
        return responses

    def pushApp(self,app):
        r = requests.get("http://%s:%d/papp/%s" % (self.address,self.port,app))
        return r

    def funcCapacityReq(self,f):
        r = requests.get("http://%s:%d/fcrq/%d" % (self.address,self.port,f))
        return r

    def funcRespCheck(self,f):
        r = requests.get("http://%s:%d/frcc/%d" % (self.address,self.port,f))
        return r

    def sendTraffic(self,traffic,function):
        print("")

    def checkResult(self,query):
        print("")
