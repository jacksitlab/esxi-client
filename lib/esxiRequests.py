from os import stat




class EsxiRequests:


    @staticmethod
    def Login(username, password):
        return ('<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" '+
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'+
                '<Header>'+
                    '<operationID>{}</operationID>'+
                '</Header>'+
                '<Body>'+
                    '<Login xmlns="urn:vim25">'+
                        '<_this type="SessionManager">ha-sessionmgr</_this>'+
                        '<userName>{}</userName>'+
                        '<password>{}</password>'+
                        '<locale>en-US</locale>'+
                    '</Login>'+
                '</Body></Envelope>').format('esxui-4863',username,password)

    @staticmethod
    def CreateGuestInfos():
        return ('<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'+
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

    @staticmethod
    def CreateHostInfos():
        return ('<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" '+
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'+
            '<Header>'+
                '<operationID>esxui-ef7</operationID>'+
            '</Header>'+
            '<Body>'+
                '<CreateContainerView xmlns="urn:vim25">'+
                    '<_this type="ViewManager">ViewManager</_this>'+
                    '<container type="Folder">ha-folder-root</container>'+
                    '<type>HostSystem</type>'+
                    '<recursive>true</recursive>'+
                '</CreateContainerView>'+
            '</Body></Envelope>')

    @staticmethod
    def RequestGuestInfos(sessionkey):
        return ('<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
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

    @staticmethod
    def RequestHostInfos(sessionkey):
        return ('<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'+
            '<Header>'+
                '<operationID>esxui-e76</operationID>'+
            '</Header>'+
            '<Body>'+
                '<RetrievePropertiesEx xmlns="urn:vim25">'+
                    '<_this type="PropertyCollector">ha-property-collector</_this>'+
                    '<specSet>'+
                        '<propSet>'+
                            '<type>HostSystem</type>'+
                            '<all>false</all>'+
                            '<pathSet>summary.hardware</pathSet>'+
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
            '</Body>'+
        '</Envelope>').format(sessionkey)