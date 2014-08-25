import threading
import time
import httphandler
import contract

class CachedJSON(object):
    _instance = None

    def __new__(self):
        if not self._instance:
            self.Jwallet = httphandler.getWallet()
            self.Jcontracts = httphandler.getContracts()
            self.Jtransaction = httphandler.getTransaction()
            self.Jorders = httphandler.getOrders()
            self.dict = {}
            self.timeStamp = time.time()
            for con in self.Jcontracts:
                self.dict[con['Id']] = con

            self._instance = super(CachedJSON, self).__new__(
                                self)
        return self._instance

    def setRefresh(self, item, duration):
        if item == 'Wallet':
            self.Jwallet = httphandler.getWallet()
        elif item == 'Contracts':
            self.Jcontracts = httphandler.getContracts()
        elif item == 'Transaction':
            self.Jtransaction = httphandler.getTransaction()
        elif item == 'Orders':
            self.Jorders = httphandler.getOrders()
        threading.Timer(duration, self.setRefresh, [item, duration]).start()


class CachedDict(object):
    _instance = None

    def __new__(self):
        if not self._instance:
            loc = CachedJSON().Jcontracts

            Max = "reach"
            Min = "fall under"
            End = "more than"
            Above = "above the previous"
            Below = "below the previous"

            silverMax = []
            silverMin = []
            silverEnd = []

            goldMax = []
            goldMin = []
            goldEnd = []

            dowBelow = []
            dowAbove = []

            silverList = {'Max' : silverMax, 'Min' : silverMin, 'End' : silverEnd }
            goldList = {'Max' : goldMax, 'Min' : goldMin, 'End' : goldEnd }
            dowList = {'Above' : dowAbove, 'Below' : dowBelow }

            self.ID = {} # Dictionary [Id -> Contract]
            i = 0
            for con in loc:
                if "Silver" in con['Name']:
                    if Max in con['Name']:
                        silverMax.append(dict2Contract(con))
                    elif Min in con['Name']:
                        silverMin.append(dict2Contract(con))
                    elif End in con['Name']:
                        silverEnd.append(dict2Contract(con))
                elif "Gold" in con['Name']:
                    if Max in con['Name']:
                        goldMax.append(dict2Contract(con))
                    elif Min in con['Name']:
                        goldMin.append(dict2Contract(con))
                    elif End in con['Name']:
                        goldEnd.append(dict2Contract(con))
                elif "Dow" in con['Name']:
                    if Above in con['Name']:
                        dowAbove.append(dict2Contract(con))
                    elif Below in con['Name']:
                        dowBelow.append(dict2Contract(con))
                self.ID[con['Id']] = con

            self.Traded = {'Silver' : silverList, 'Gold' : goldList, 'Dow' : dowList }
            self._instance = super(CachedDict, self).__new__(
                                self)
        return self._instance
    
def dict2Contract(d):
    conID = d['Id']
    name = d['Name']
    underlying = d['Name'].split()[0]
    if underlying == 'Dow':
        K = contract.findDowStrike(name)
    else:
        K = float(d['Name'].split('$')[1].split('/')[0])
    expiry = time.strptime(d['EventDate'], "%Y-%m-%dT%H:%M:%S")
    return contract.Contract(conID, name, underlying, K, expiry)
    
