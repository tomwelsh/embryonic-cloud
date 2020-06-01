import apiClient
import json


app=[1,2,3,4]
data=2
client = apiClient.APIClient("127.0.0.1",5000)
print(client.checkAPI().text)
print("Options:\n1) Function Resp Check\n2)Function Capacity Request\n3)App Test")
ch=0
while ch!=str(99):
    ch=input("selection>")
    if ch =='1':
        f=input("function")
        print(client.funcRespCheck(int(f)).text)
    elif ch =='2':
        f=input("function")
        print(client.funcCapacityReq(int(f)).text)
    elif ch=='3':
        client.checkAppRequest(app,150)
    elif ch=='4':
        client.pushApp(json.dumps([app,data]))
    elif ch=='5':
        client.checkAppRequest([1,12,8,9,3,5,6],150)
    elif ch=='6':
        client.pushApp(json.dumps([[1,12,8,9,3,5,6],1]))
    elif ch == '99':
        quit()
    else:
        print("invalid input")



#add app
#traffic to and from app
#   usecases:
#       -cryptograph?
#       -text parsing
#       -video streaming
#cell differentiate with function timeout
#cell destruction
