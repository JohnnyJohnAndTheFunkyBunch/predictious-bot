
import urllib
import re
import HTMLParser
import xml.etree.ElementTree as ET
import time


# root google finance api string -> float

def find_data(root, parameter):
    leaf = root[0].find(parameter).attrib['data']
    if leaf == "":
        return 'No Data'
    else:
        return float(leaf)

def get_dji_close(): # change get_dji, since duplicate code
    'returns the real time price of DJI'
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + '.DJI').read()
    n = re.search('id="ref_' + google_id + '_l".*?>(.*?)<', content)
    m = re.search('id="ref_' + google_id + '_c".*?>(.*?)<', content) #change the id reference, go to google page and inspect element
    spot = n.group(1)
    adder = m.group(1)
    spot = float(spot.replace(",",""))
    
    if adder[0] == '+':
        return spot - float(adder[1:])
    elif adder[0] == '-':
        return spot + float(adder[1:])
    else:
        return spot
    
#This ID is for getting the DJI index real time, incase google changes their things
google_id = '983582'

goldSpot = 'http://www.bloomberg.com/quote/XAUUSD:CUR'
silverSpot = 'http://www.bloomberg.com/quote/XAGUSD:CUR'

def get_gold():
    base_url = 'http://www.bloomberg.com/quote/XAUUSD:CUR'
    content = urllib.urlopen(base_url).read()
    anchor = '<span class=" price">'
    anchor_len = len(anchor)
    pos = content.index('<span class=" price">')
    content = content[pos + 30:pos + 50]
    content = content.replace(",","")
    m = re.match(r'\d+.\d+', content).group()
    return float(m)

def get_silver():
    base_url = 'http://www.bloomberg.com/quote/XAGUSD:CUR'
    content = urllib.urlopen(base_url).read()
    anchor = '<span class=" price">'
    anchor_len = len(anchor)
    pos = content.index('<span class=" price">')
    content = content[pos + 30:pos + 50]
    content = content.replace(",","")
    m = re.match(r'\d+.\d+', content).group()
    return float(m)

def get_gold_vol():
    base_url = 'http://finance.yahoo.com/q?s=%5EGVZ'
    content = urllib.urlopen(base_url).read()
    anchor = '<span id="yfs_l10_^gvz">'
    anchor_len = len(anchor)
    pos = content.index(anchor)
    content = content[pos + anchor_len:pos + anchor_len + 20]
    content = content.replace(",","")
    m = re.match(r'\d+.\d+', content).group()
    return float(m)

""" 
def get_silver_vol():
    base_url = 'http://www.cboe.com/DelayedQuote/SimpleQuote.aspx?ticker=VXSLV'
    content = urllib.urlopen(base_url).read()
    anchor = '<span class="delayedQuotesShortH2Black">'
    anchor_len = len(anchor)
    m = re.search(anchor + '\d+.\d+',content).group(0)
    return float(m[anchor_len:anchor_len + 5])
"""

def get_silver_vol():
    base_url = 'http://finance.yahoo.com/q?s=%5EVXSLV'
    content = urllib.urlopen(base_url).read()
    anchor = '<span id="yfs_l10_^vxslv">'
    anchor_len = len(anchor)
    pos = content.index(anchor)
    content = content[pos + anchor_len:pos + anchor_len + 20]
    content = content.replace(",","")
    m = re.match(r'\d+.\d+', content).group()
    return float(m)

def get_dji():
    'returns the real time price of DJI'
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + '.DJI').read()
    m = re.search('id="ref_' + google_id + '_l".*?>(.*?)<', content) #change the id reference, go to google page and inspect element
    if m:
        quote = m.group(1)
    else:
        quote = 'no quote available for: ' + '.DJI'
    return float(quote.replace(",","")) # take out the ",", then turn it into float


# still having problmes with volatility (NOT FINISH) Use 15 minute delay one
def get_vxd():
    'returns the real time VXD'
    # goes to the site, looks at the source page, finds when it shows the price, and gets it
    base_url = 'http://data.cnbc.com/quotes/.VXD'
    content = urllib.urlopen(base_url).read()
    substring = '"DJIA VOLATILITY","shortName":"VXD","last":"'
    numba = content.find(substring)
    adder = len(substring)
    return float(content[numba+adder:numba+adder+5])
    #m = re.search('<span data-field="last" class="price">.*?>(.*?)<', content)
    #if m:
    #    quote = m.group(1)
    #else:
    #    quote = 'no quote available for: ' + '.DJI'
    #return quote

def updateSpot(ul):
    f = open('../log/prices.log', 'r+')
    dji_price = float(f.readline())
    gold_price = float(f.readline())
    silver_price = float(f.readline())
    new_dji_price = get_dji()
    if new_dji_price > dji_price:
        dji_price = new_dji_price
    new_gold_price = kitco()
    if new_gold_price > gold_price:
        gold_price = new_gold_price
    new_silver_price = get_silver()
    if new_silver_price > silver_price:
        silver_price = new_silver_price
    f.seek(0)
    f.truncate()
    f.write(str(dji_price) + '\n' + str(gold_price) + '\n' + str(silver_price) + '\n')
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime() + '\n')
    f.write(timestamp)
    if ul == 'Dow':
        return new_dji_price
    elif ul == 'Silver':
        return new_silver_price
    elif ul == 'Gold':
        return new_gold_price
    


# Str -> Float
def getSpot(ul):
    if ul == 'Dow':
        return get_dji()
    elif ul == 'Silver':
        return get_silver()
    elif ul == 'Gold':
        return get_gold()
    
# Str -> Float
def getVol(ul):
    if ul == 'Dow':
        return get_vxd()
    elif ul == 'Silver':
        return get_silver_vol()
    elif ul == 'Gold':
        return get_gold_vol()


def kitco():
    base_url = 'http://www.kitco.com/market/'
    content = urllib.urlopen(base_url).read()
    anchor = 'GOLD</a></td>'
    anchor_len = len(anchor)
    pos = content.index('GOLD</a></td>')
    content = content[pos + anchor_len:pos + anchor_len + 500]
    i = 0
    while i < 3:
        anchor = '<td>'
        pos = content.index('<td>')
        content = content[pos + 4 :pos + 300]
        i = i + 1
    return float(content[:7])

if __name__ == "__main__":
    previous = time.time()
    """
    print "Dow Spot: " + str(getSpot('Dow'))
    print 'Time: ' + str(time.time() - previous)
    previous = time.time()
    """
    print "Silver Spot: " + str(getSpot('Silver'))
    print 'Time: ' + str(time.time() - previous)
    previous = time.time()
    print "Gold Spot: " + str(getSpot('Gold'))
    print 'Time: ' + str(time.time() - previous)
    previous = time.time()
    """
    print "Dow Vol: " + str(getVol('Dow'))
    print 'Time: ' + str(time.time() - previous)
    previous = time.time()
    """
    print "Silver Vol: " + str(getVol('Silver'))
    print 'Time: ' + str(time.time() - previous)
    previous = time.time()
    print "Gold Vol: " + str(getVol('Gold'))
    print 'Time: ' + str(time.time() - previous)
