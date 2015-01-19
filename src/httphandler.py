import urllib2
import json
import time

f = open('../key.txt', 'r')
key = f.read()

# GET:
ordersURL = 'https://api.predictious.com/v1/orders'
walletURL = 'https://api.predictious.com/v1/wallet'
transactionsURL = 'https://api.predictious.com/v1/transactions'
contractsURL = 'https://api.predictious.com/v1/contracts'
contractordersURL =  'https://api.predictious.com/v1/contractorders'

# POST:
addordersURL = 'https://api.predictious.com/v1/addorders'
cancelordersURL = 'https://api.predictious.com/v1/cancelorders'

# GET FUNCTIONS
# Void -> List of Dictionaries
def getOrders():
    req = urllib2.Request(ordersURL)
    req.add_header('X-Predictious-Key', key)
    resp = urllib2.urlopen(req)
    content = resp.read()
    j = json.loads(content)
    return j

def getWallet():
    req = urllib2.Request(walletURL)
    req.add_header('X-Predictious-Key', key)
    resp = urllib2.urlopen(req)
    content = resp.read()
    j = json.loads(content)
    return j

def getTransaction():
    req = urllib2.Request(transactionsURL)
    req.add_header('X-Predictious-Key', key)
    resp = urllib2.urlopen(req)
    content = resp.read()
    j = json.loads(content)
    return j

def getContracts():
    req = urllib2.Request(contractsURL)
    req.add_header('X-Predictious-Key', key)
    resp = urllib2.urlopen(req)
    content = resp.read()
    j = json.loads(content)
    return j

def getContractOrders(conID):
    req = urllib2.Request(contractordersURL + '/' +conID)
    req.add_header('X-Predictious-Key', key)
    resp = urllib2.urlopen(req)
    content = resp.read()
    j = json.loads(content)
    return j


# POST FUNCTIONS



# String -> Array of String (ID shiets)
def postAddOrders(data):
    headers = {'Content-Type': 'application/json', 'X-Predictious-Key': key, 'Accept': 'application/json', 'Accept-Encoding':'gzip,deflate', 'Content-Length':0, 'User-Agent':'runscope/0.1'}
    req = urllib2.Request(addordersURL, data, headers)
    resp = urllib2.urlopen(req)
    content = resp.read()
    print content
    return content
    
    
# Array of String (ID) -> Array of Boolean (Success?)
def postCancelOrders(data):
    print data
    headers = {'Content-Type': 'application/json', 'X-Predictious-Key': key, 'Accept': 'application/json', 'Accept-Encoding':'gzip,deflate', 'Content-Length':0, 'User-Agent':'runscope/0.1'}
    req = urllib2.Request(cancelordersURL, data, headers)
    resp = urllib2.urlopen(req)
    content = resp.read()
    return content



if __name__ == "__main__":
    """
    previous = time.time()
    j = getWallet()
    print 'Get Orders...'
    print 'Time: ' + str(time.time() - previous)
    previous = time.time()
    j = getWallet()
    print 'Get Wallet...'
    print 'Time: ' + str(time.time() - previous)
    previous = time.time()
    j = getTransaction()
    print 'Get Transaction....'
    print 'Time: ' + str(time.time() - previous)
    previous = time.time()
    j = getContracts()
    print 'Get Contract...'
    print 'Time: ' + str(time.time() - previous)
    """
    print postAddOrders("234")






