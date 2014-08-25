
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
    gold_end = algo.Algo(\
            objectcache.CachedDict().Traded['Gold']['End'],\
            5,\
            100000,\
            30,\
            "GoldEnd")
    silver_end = algo.Algo(\
            objectcache.CachedDict().Traded['Silver']['End'],\
            5,\
            100000,\
            30,\
            "SilverEnd")
    dow_above = algo.Algo(\
            objectcache.CachedDict().Traded['Dow']['Above'],\
            5,\
            100000,\
            30,\
            "DowAbove")
    thread_gold = Thread(target = gold_end.algo, args = [])
    thread_silver = Thread(target = silver_end.algo, args = [])
    thread_gold.daemon = True
    thread_silver.daemon = True
    thread_gold.start()
    time.sleep(60)
    thread_silver.start()

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
