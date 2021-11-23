import argparse
import urllib3
import getpass
import json
import yaml
from lib.loginResponse import LoginResponse
from lib.createVmInfoResponse import CreateVmInfoResponse
from lib.getVmInfoResponse import GetVmInfoResponse
from lib.getHostInfoResponse import GetHostInfoResponse
from lib.summaryData import SummaryData
from lib.esxiRequests import EsxiRequests

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.114 Safari/537.36"
urllib3.disable_warnings()
COMMAND_GET_HOSTINFOS="get-host"
COMMAND_GET_GUESTINFOS="get-guests"
COMMAND_GET_ALLINFOS="get-all"
COMMAND_TEST_CONNECTION="test"

class EsxiClient:

    def __init__(self, host, username, password, scheme="https", port=443):
        self.host = host
        self.credentials = dict(username=username, password=password)
        self.scheme = scheme
        self.port = port
        self.loginData = None

    def login(self):
        response = self.requestRest('POST','/sdk/',EsxiRequests.Login(self.credentials['username'],self.credentials['password']))
#        print(response)
        if response["code"] == 200:
            self.loginData = LoginResponse(response['content'],response['headers'])
            return True
        else:
            return False

    def createGuestInfos(self):
        response = self.requestRest('POST', '/sdk/',EsxiRequests.CreateGuestInfos())
        if response['code'] == 200:
            data = CreateVmInfoResponse(response['content'])
            return data.sessionKey
        return None

    def createHostInfos(self):
        response = self.requestRest('POST', '/sdk/',EsxiRequests.CreateHostInfos())
        if response['code'] == 200:
            data = CreateVmInfoResponse(response['content'])
            return data.sessionKey
        return None

    def getGuestInfos(self, sessionkey):
        response = self.requestRest('POST','/sdk/',EsxiRequests.RequestGuestInfos(sessionkey))
        if response['code']==200:
            return GetVmInfoResponse(response['content'])
        return None

    def getHostInfos(self, sessionkey):
        response = self.requestRest('POST','/sdk/',EsxiRequests.RequestHostInfos(sessionkey))
        if response['code']==200:
            return GetHostInfoResponse(response['content'])
        return None


    def requestRest(self, method, url, data=None, headers=dict()):
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url='{}://{}{}'.format(self.scheme, self.host, url)
        headers["Content-Type"]="text/xml"
        headers["Accept="]=": */*"
        headers["Referer"]="{}://{}/ui/".format(self.scheme,self.host)
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

    def runCommand(self, cmd, of):
        if cmd == COMMAND_GET_GUESTINFOS:
            self.login()
            key = self.createGuestInfos()
            data = self.getGuestInfos(key)
            self.printData(data, of)
        elif cmd == COMMAND_GET_HOSTINFOS:
            self.login()
            key = self.createHostInfos()
            data = self.getHostInfos(key)
            self.printData(data, of)
        elif cmd == COMMAND_GET_ALLINFOS:
            self.login()
            key = self.createGuestInfos()
            data=SummaryData()
            data.setGuests(self.getGuestInfos(key))
            key = self.createHostInfos()
            data.setHost(self.getHostInfos(key))
            self.printData(data, of)
        elif cmd == COMMAND_TEST_CONNECTION:
            success= self.login()
            msg="Login succeeded" if success else "Login failed"
            self.printData(dict(msg=msg), of)
        else:
            self.printData(dict(msg="command '{}' not yet implemented".format(cmd)), of)

    def printData(self, data, of):
        if of == "json":
            print(json.dumps(data.toDict()))
        elif of == "yaml":
            print(yaml.dump(data.toDict()))
        elif of == "str":
            print(str(data))
        else:
            print("unknown outputformat {}".format(of))

parser = argparse.ArgumentParser(description='Esxi http client')
parser.add_argument('--host', action='store', required=True, type=str, help='hostname or ip address of the esxi server')
parser.add_argument('--username', action='store', required=True, type=str, help='username')
parser.add_argument('--password', action='store', required=False, type=str, help='user password')
parser.add_argument('--output-format', action='store', required=False, type=str, help='select an output format',default="str", choices=["json", "yaml", "str"])
parser.add_argument('command', action='store', nargs=1, default=None, choices=[COMMAND_GET_ALLINFOS, COMMAND_GET_HOSTINFOS, COMMAND_GET_GUESTINFOS, COMMAND_TEST_CONNECTION])
args = parser.parse_args()
passwd = args.password
if passwd is None:
    passwd = getpass.getpass("Please enter password:")
client = EsxiClient(args.host,args.username,passwd)
client.runCommand(args.command[0], args.output_format)

