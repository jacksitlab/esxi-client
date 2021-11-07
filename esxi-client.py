import urllib3
import certifi
from lib.loginResponse import LoginResponse
from lib.createVmInfoResponse import CreateVmInfoResponse
urllib3.disable_warnings()
import sys

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.114 Safari/537.36"

class EsxiClient:

    def __init__(self, host, username, password, scheme="https", port=443):
        self.host = host
        self.credentials = dict(username=username, password=password)
        self.scheme = scheme
        self.port = port
        self.loginData = None

    def login(self):
        payload='<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>{}</operationID></Header><Body><Login xmlns="urn:vim25"><_this type="SessionManager">ha-sessionmgr</_this><userName>{}</userName><password>{}</password><locale>en-US</locale></Login></Body></Envelope>'.format('esxui-4863',self.credentials['username'],self.credentials['password'])
        response = self.requestRest('POST','/sdk/',payload)
#        print(response)
        if response["code"] == 200:
            self.loginData = LoginResponse(response['content'],response['headers'])
            return True
        else:
            return False

    def createGuestInfos(self):
        payload = ('<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'+
            '<Header>'+
                '<operationID>esxui-8cc9</operationID>'+
            '</Header>'+
            '<Body>'+
                '<CreateContainerView xmlns="urn:vim25">'+
                    '<_this type="ViewManager">ViewManager</_this>'+
                    '<container type="Folder">ha-folder-root</container>'+
                    '<type>VirtualMachine</type>'+
                    '<recursive>true</recursive>'+
                '</CreateContainerView>'+
            '</Body></Envelope>')
        response = self.requestRest('POST', '/sdk/',payload)
        if response['code'] == 200:
            data = CreateVmInfoResponse(response['content'])
            return data.sessionKey
        return None

    def getGuestInfos(self, sessionkey):
        payload = ('<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
            '<Header><operationID>esxui-f633</operationID></Header>' +
            '<Body>'+
                '<RetrievePropertiesEx xmlns="urn:vim25">'+
                    '<_this type="PropertyCollector">ha-property-collector</_this>'+
                    '<specSet>'+
                        '<propSet>'+
                            '<type>VirtualMachine</type>'+
                            '<all>false</all>'+
                            '<pathSet>name</pathSet>'+
                            '<pathSet>config.annotation</pathSet>'+
                            '<pathSet>config.defaultPowerOps</pathSet>'+
                            '<pathSet>config.extraConfig</pathSet>'+
                            '<pathSet>config.hardware.memoryMB</pathSet>'+
                            '<pathSet>config.hardware.numCPU</pathSet>'+
                            '<pathSet>config.hardware.numCoresPerSocket</pathSet>'+
                            '<pathSet>config.guestId</pathSet>'+
                            '<pathSet>config.guestFullName</pathSet>'+
                            '<pathSet>config.version</pathSet>'+
                            '<pathSet>config.template</pathSet>'+
                            '<pathSet>datastore</pathSet>'+
                            '<pathSet>guest</pathSet>'+
                            '<pathSet>runtime</pathSet>'+
                            '<pathSet>summary.storage</pathSet>'+
                            '<pathSet>summary.runtime</pathSet>'+
                            '<pathSet>summary.quickStats</pathSet>'+
                            '<pathSet>effectiveRole</pathSet>'+
                        '</propSet>'+
                        '<objectSet>'+
                        '<obj type="ContainerView">{}</obj>'+
                        '<skip>true</skip>'+
                        '<selectSet xsi:type="TraversalSpec">'+
                            '<name>view</name>'+
                            '<type>ContainerView</type>'+
                            '<path>view</path>'+
                            '<skip>false</skip>'+
                        '</selectSet>'+
                    '</objectSet>'+
                '</specSet>'+
                '<options/>'+
            '</RetrievePropertiesEx>'+
        '</Body></Envelope>').format(sessionkey)
        response = self.requestRest('POST','/sdk/',payload)
        return response

    def getToken(self):
        self.csrfToken = "q7ep2b0cql5rfxuz5514jhyz8i5errjl"
        pass

    def requestRest(self, method, url, data=None, headers=dict()):
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url='{}://{}{}'.format(self.scheme, self.host, url)
        headers["Content-Type"]="text/xml"
        headers["Accept="]=": */*"
        headers["Referer"]="https://10.20.4.89/ui/"
        headers["Host"]=self.host
        headers["User-Agent"]=USER_AGENT
        headers["SOAPAction"]="urn:vim25/s55741"
        headers["Connection"]="keep-alive"
        if self.loginData is not None:
            headers['Cookie']=self.loginData.getCookie()
        r = None
        if data == None:
            r = http.request(method, url, headers=headers)
        else:
            encoded_data = data.encode('utf-8')
#            print("payload="+str(encoded_data))
            r = http.request(method, url, body=encoded_data, headers=headers)
        return dict(code=r.status, content = r.data.decode('utf-8'), headers=r.headers)

args = sys.argv
args.pop(0)
client = EsxiClient(args[0],args[1],args[2])
client.login()
key = client.createGuestInfos()
data = client.getGuestInfos(key)
print(data)