
from .baseXmlResponse import BaseXmlResponse

class BaseVmWareXmlResponse(BaseXmlResponse):

    def findPropertySet(self, root, name):
        sets = self.getSubTrees(root,'propSet')
        if sets is None:
            return None
        for set in sets:
            nameElem = self.getSubTree(set,'name')
            if nameElem is not None and nameElem.text == name:
                return set
        return None

    def findPropertySetValue(self, root, name, toString=True):
        set = self.findPropertySet(root, name)
        if set is not None:
            val = self.getSubTree(set,'val')
            if toString:
                return val.text if val is not None  else None
            else:
                return val
        return None