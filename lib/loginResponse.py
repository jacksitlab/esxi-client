import xml.etree.ElementTree as ET
from .baseXmlResponse import BaseXmlResponse

class LoginResponse(BaseXmlResponse):

    def __str__(self):
        return ('LoginResponse[key={} userName={} fullName={} loginTime={} lastActiveTime={} locale={} messageLocale={} '+
        'extensionSession={} ipAddress={} userAgent=\'{}\' callCount={} headers={}]').format(self.key,self.userName, self.fullName, self.loginTime, 
            self.lastActiveTime, self.locale, self.messageLocale, self.extensionSession, self.ipAddress, self.userAgent, self.callCount, self.headers)
    def __init__(self, response, headers):
        data = ET.fromstring(response)
        innerData = self.getSubTreeByTree(
            data, ['Body', 'LoginResponse', 'returnval'])
        if innerData is None:
            raise ValueError('no know response data found')
        
        self.key = self.getSubTree(innerData,'key').text
        self.userName = self.getSubTree(innerData,'userName').text
        self.fullName = self.getSubTree(innerData,'fullName').text
        self.loginTime = self.getSubTree(innerData,'loginTime').text
        self.lastActiveTime = self.getSubTree(innerData,'lastActiveTime').text
        self.locale = self.getSubTree(innerData,'locale').text
        self.messageLocale = self.getSubTree(innerData,'messageLocale').text
        self.extensionSession = self.getSubTree(innerData,'extensionSession').text
        self.ipAddress = self.getSubTree(innerData,'ipAddress').text
        self.userAgent = self.getSubTree(innerData,'userAgent').text
        self.callCount = self.getSubTree(innerData,'callCount').text
        self.headers = headers
        print(self)

    def getCookie(self):
        key="Set-Cookie"
        if key in self.headers:
            return self.headers[key]
        return ""
