import xml.etree.ElementTree as ET
from .baseXmlResponse import BaseXmlResponse
from .baseVmWareXmlResponse import BaseVmWareXmlResponse

class GuestVmInfo(BaseVmWareXmlResponse):

    def __str__(self):
        return "GuestVmInfo[vmId={} name={} os={} mem={} vCores={} hdd={} ipAddresses={} state={}]".format(self.vmId, 
            self.name, self.os, self.memory, self.cps*self.cpu, self.hdd, self.ipAddresses, self.powerState)
    def toDict(self):
        return dict(id=self.vmId, name=self.name, os=self.os, memory=self.memory, vCPUs=self.cps*self.cpu, 
            hdd=self.hdd, ipAddresses=self.ipAddresses, state=self.powerState)

    def __init__(self, xmlRoot):
        self.vmId = self.getChildwithAttr(xmlRoot,'obj','type','VirtualMachine').text
        self.name = self.findPropertySetValue(xmlRoot, 'name')
        self.xtraConfig = self.findPropertySet(xmlRoot,'config.extraConfig')
        self.details = self.findPropertySetValue(xmlRoot, 'guest', False)
        self.hdd = self.getHdd(xmlRoot)
        self.ipAddresses= self.getIpAddresses(self.details)
        self.powerState = self.getPowerState(self.details)
        self.os = self.findPropertySetValue(xmlRoot, 'config.guestFullName')
        self.memory = self.findPropertySetValue(xmlRoot, 'config.hardware.memoryMB')
        self.cpu = int(self.findPropertySetValue(xmlRoot, 'config.hardware.numCPU'))
        self.cps = int(self.findPropertySetValue(xmlRoot, 'config.hardware.numCoresPerSocket'))

    def getPowerState(self, details):
        return self.getSubTree(details,'guestState').text

    def getIpAddresses(self, details):
        adr=[]
        tmp = self.getSubTrees(self.getSubTree(details,'net'),'ipAddress')
        if tmp is not None:
            for a in tmp:
                adr.append(a.text)
        return adr

    def getHdd(self, xmlRoot):
        tmp=self.getSubTree(self.findPropertySetValue(xmlRoot, 'summary.storage', False),'committed')
        return int(tmp.text) if tmp is not None else 0



class GetVmInfoResponse(BaseXmlResponse):

    def __str__(self):
        s=[]
        for g in self.guests:
            s.append("{}".format(g))
        return ('GetVmInfoResponse[guests={}]').format(s)
    def toDict(self):
        root = dict()
        root['guests']=[]
        for guest in self.guests:
            root['guests'].append(guest.toDict())
        return root
    def __init__(self, response):
        data = ET.fromstring(response)
        innerData = self.getSubTreeByTree(
            data, ['Body', 'RetrievePropertiesExResponse', 'returnval'])
        if innerData is None:
            raise ValueError('no know response data found')
        
        self.guests=[]
        for child in innerData:
            vmId = self.getChildwithAttr(child,'obj','type','VirtualMachine')
            if vmId is not None:
                self.guests.append(GuestVmInfo(child))



