import xml.etree.ElementTree as ET
from .baseXmlResponse import BaseXmlResponse

class CreateVmInfoResponse(BaseXmlResponse):

    def __str__(self):
        return ('CreateVmInfoResponse[sessionKey={}]').format(self.sessionKey)
    def __init__(self, response):
        data = ET.fromstring(response)
        innerData = self.getSubTreeByTree(
            data, ['Body', 'CreateContainerViewResponse', 'returnval'])
        if innerData is None:
            raise ValueError('no know response data found')
        
        self.sessionKey = innerData.text
        print(self)

