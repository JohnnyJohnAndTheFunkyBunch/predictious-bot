
import sys
import algo
import wallet
import httphandler
import order
from threading import Thread
import objectcache
import time

algo_threads = []

def startDaAlgo():
    global algo_threads
    dow_above = algo.Algo(\
            objectcache.CachedDict().Traded['Dow']['Above'],\
            5,\
            100000,\
            30,\
            "DowAbove")
    thread_dow = Thread(target = dow_above.algo, args = [])
    thread_dow.daemon = True
    thread_dow.start()
    dow_below = algo.Algo(\
            objectcache.CachedDict().Traded['Dow']['Below'],\
            5,\
            100000,\
            30,\
            "DowBelow")
    time.sleep(20)
    thread_dow2 = Thread(target = dow_below.algo, args = [])
    thread_dow2.daemon = True
    thread_dow2.start()

def threadManager():
    # Reads in config file every half a second, see if anything changes
    # Apply changes accordingly like deleting threads
    f = open('../log/algo.log', 'r')
    f.readline()
    param_name = (f.readline()).split(',')
    

if __name__ == "__main__":
    startDaAlgo()
    #displayThreads()
    while(1):
        time.sleep(1)
