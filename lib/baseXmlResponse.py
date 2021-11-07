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
