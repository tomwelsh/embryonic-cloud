#this is the server (cell) side API

from flask import Flask
import flask_restful


class HelloWorld(flask_restful.Resource):

    def get(self):
        return {'hello': 'world'}


class funcRespCheck(flask_restful.Resource):
    #A client sends a esource template for their proposed application
    #   put appLoadReq{R1,R2,R3} etc
    #The Cell responds with a request ID (hash)
    #The client can then check on the state of the request
    #   get{id:HASH}

    def get(self,f):
        print(eAPI.cell.node.checkFunc(f))
        if  eAPI.cell.node.checkFunc(f) > 0:
            return {'found': f}
        else:
            return {'not found':f}

class funcCapReq(flask_restful.Resource):

    def get(self,f):
        eAPI.cell.node.apiHandler({'typ':"PFRQ",'func':f}) #API FUNCTION REQUEST MESSAGE
        return {'Requested':f}


class pushApp(flask_restful.Resource):

    def get(self,app):                  #this should be a PUT really....
        eAPI.cell.node.apiHandler({'typ':"PAPP",'pl':app}) #API FUNCTION REQUEST MESSAGE
        return {'Pushed':app}

class embroynicAPI():

    def __init__(self):
        #self.cell=cell
        self.app = Flask(__name__)
        self.api = flask_restful.Api(self.app)
        self.addResources()

    def addCellRef(self,cell):
        self.cell=cell

    def startAPI(self):
        self.app.run()

    def addResources(self):
        self.api.add_resource(HelloWorld, '/')
        self.api.add_resource(funcCapReq, '/fcrq/<int:f>')
        self.api.add_resource(funcRespCheck, '/frcc/<int:f>')
        self.api.add_resource(pushApp, '/papp/<string:app>')




eAPI=embroynicAPI()


#eAPI.app.run(port='5002')
