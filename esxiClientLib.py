import urllib3
from .lib.loginResponse import LoginResponse
from .lib.createVmInfoResponse import CreateVmInfoResponse
from .lib.getVmInfoResponse import GetVmInfoResponse
from .lib.getHostInfoResponse import GetHostInfoResponse
from .lib.summaryData import SummaryData
from .lib.esxiRequests import EsxiRequests

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.114 Safari/537.36"
urllib3.disable_warnings()
class EsxiClient:

    def __init__(self, host, username, password, scheme="https", port=443):
        self.host = host
        self.credentials = dict(username=username, password=password)
        self.scheme = scheme
        self.port = port
        self.loginData = None

    def _login(self):
        response = self.requestRest('POST','/sdk/',EsxiRequests.Login(self.credentials['username'],self.credentials['password']))
#        print(response)
        if response["code"] == 200:
            self.loginData = LoginResponse(response['content'],response['headers'])
            return True
        else:
            return False

    def _createGuestInfos(self):
        response = self.requestRest('POST', '/sdk/',EsxiRequests.CreateGuestInfos())
        if response['code'] == 200:
            data = CreateVmInfoResponse(response['content'])
            return data.sessionKey
        return None

    def _createHostInfos(self):
        response = self.requestRest('POST', '/sdk/',EsxiRequests.CreateHostInfos())
        if response['code'] == 200:
            data = CreateVmInfoResponse(response['content'])
            return data.sessionKey
        return None

    def _getGuestInfos(self, sessionkey):
        response = self.requestRest('POST','/sdk/',EsxiRequests.RequestGuestInfos(sessionkey))
        if response['code']==200:
            return GetVmInfoResponse(response['content'])
        return None

    def _getHostInfos(self, sessionkey):
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

    def getGuestInfos(self):
        self._login()
        key = self._createGuestInfos()
        data = self._getGuestInfos(key)
        return data

    def getHostInfos(self):
        self._login()
        key = self._createHostInfos()
        data = self._getHostInfos(key)
        return data
    
    def getAllInfos(self):
        self._login()
        key = self._createGuestInfos()
        data=SummaryData()
        data.setGuests(self._getGuestInfos(key))
        key = self._createHostInfos()
        data.setHost(self._getHostInfos(key))
        return data

    def testConnection(self):
        success= self._login()
        msg="Login succeeded" if success else "Login failed"
        return dict(success=success, msg=msg)



