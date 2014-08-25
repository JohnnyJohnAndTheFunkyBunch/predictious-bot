import httphandler

class Wallet:
    def __init__(self):
        j = httphandler.getWallet()
        self.totalFunds = j['TotalFunds']
        self.availableFunds = j['AvailableFunds']
        self.shares = {}
        for con in j['Shares']:
            self.shares[con['ContractId']] = con['Quantity']

