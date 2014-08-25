import httphandler
import time
import data
import calendar
import black

Max = "reach"
Min = "fall under"
End = "more than"
Above = "above the previous"
Below = "below the previous"

############## Class Contract ##################

class Contract:
    def __init__(self, conID, name, underlying, K, expiry):
        self.conID = conID
        self.name = name
        self.underlying = underlying
        self.K = float(K)
        self.expiry = expiry # struct_time
    def __repr__(self):
        return self.name + "\n"
    def calculate(self):
        S = data.getSpot(self.underlying)
        K = self.K
        sigma = data.getVol(self.underlying)/100
        tenor = black.get_tenor(float(calendar.timegm(self.expiry)))
        #print "========================="
        #print "BlackScholes Parameters:"
        #print "Spot: " + str(S)
        #print "K: " + str(K)
        #print "sigma: " + str(sigma)
        #print "tenor: " + str(tenor)
        #print "========================="
        if Max in self.name:
            return black.up_and_in_cash_at_hit_or_nothing(data.getSpot(self.underlying),
                                                          self.K,
                                                          0,
                                                          data.getVol(self.underlying)/100,
                                                          black.get_tenor(float(calendar.timegm(self.expiry))))
        elif Above in self.name:
            return black.value(data.getSpot(self.underlying),
                               self.K,
                               0,
                               data.getVol(self.underlying)/100,
                               black.get_tenor(float(calendar.timegm(self.expiry))),
                               True)
        elif Below in self.name:
            return black.value(data.getSpot(self.underlying),
                               self.K,
                               0,
                               data.getVol(self.underlying)/100,
                               black.get_tenor(float(calendar.timegm(self.expiry))),
                               False)
        else:
            return black.value(data.getSpot(self.underlying),
                               self.K,
                               0,
                               data.getVol(self.underlying)/100,
                               black.get_tenor(float(calendar.timegm(self.expiry))),
                               True)

def findDowStrike(name):
    strike = name.split()[4]
    if (strike == 'above'):
        return data.get_dji_close()
    elif (strike == 'below'):
        return data.get_dji_close()
    else:
        side = name.split()[6]
        if side == 'above':
            return data.get_dji_close() + int(strike)
        elif side == 'below':
            return data.get_dji_close() - int(strike)
    

        
#if __name__ == "__main__":
#    print "Getting all contracts"
#    g = getAll()[1]
#    for con in g['Gold']['End']:
#        print "_______________"
#        print con.name
#        print "K: " + str(con.K)
#        print "Value: " + str(con.calculate())
#        print "_______________"
#    for con in g['Dow']['Above']:
#        print "_______________"
#        print con.name
#        print "K: " + str(con.K)
#        print "Value: " + str(con.calculate())
#        print "_______________"

    
    
