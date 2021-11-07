class BaseXmlResponse:

    def getSubTreeByTree(self, root, tree=[]):
        while len(tree) > 0:
            root = self.getSubTree(root, tree.pop(0))
        return root

    def getSubTree(self, root, tagName):
        if root is None:
            return None
        for child in root:
            if child.tag.endswith(tagName):
                return child
        return None

    def getSubTrees(self, root, tagName):
        if root is None:
            return None
        s=[]
        for child in root:
            if child.tag.endswith(tagName):
                s.append(child)
        return s

    def getChildwithAttr(self, root, tagName, attributeKey, attributeValue):
        if root is None:
            return None
        for child in root:
            if child.tag.endswith(tagName):
                if attributeKey in child.attrib and child.attrib[attributeKey]==attributeValue:
                    return child
        return None