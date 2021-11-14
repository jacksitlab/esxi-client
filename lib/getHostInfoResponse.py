import xml.etree.ElementTree as ET
from .baseVmWareXmlResponse import BaseVmWareXmlResponse

class GetHostInfoResponse(BaseVmWareXmlResponse):

    def __str__(self):
        return ('GetHostInfoResponse[vendor={} model={} vCPUs={} memory={}]').format(
            self.vendor, self.model, self.vCPUs, self.memory)

    def toDict(self):
        return dict(vendor=self.vendor, model=self.model, vCPUs=self.vCPUs, memory=self.memory)

    def __init__(self, response):
        data = ET.fromstring(response)
        innerData = self.getSubTreeByTree(
            data, ['Body', 'RetrievePropertiesExResponse', 'returnval', 'objects'])
        dataSet = self.findPropertySetValue(innerData,'summary.hardware',False)
        if dataSet is None:
            print(response)
            raise ValueError('no know response data found')
        
        self.vendor = self.getSubTree(dataSet,'vendor').text
        self.model = self.getSubTree(dataSet,'model').text
        self.vCPUs = int(self.getSubTree(dataSet,'numCpuThreads').text)
        self.memory = int(self.getSubTree(dataSet,'memorySize').text)

