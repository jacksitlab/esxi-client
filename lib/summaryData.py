

class SummaryData:

    def __init__(self):
        self.host=None
        self.guests=None
        pass

    def setHost(self, host):
        self.host = host
    
    def setGuests(self, guests):
        self.guests = guests
    
    def toDict(self):
        return dict(host=self.host.toDict() if self.host is not None else None,
            guests=self.guests.toDict() if self.guests is not None else None)

    def __str__(self):
        return "SummaryData[hosts={}, guests={}]".format(str(self.host), str(self.guests))