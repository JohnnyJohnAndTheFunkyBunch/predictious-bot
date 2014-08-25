import curses
from curses import wrapper
import time
import data
import thread
import objectcache
import httphandler

gold_p = 0
silver_p = 0
max_y = 0
max_x = 0

STATE = 's'
INSTRUMENT = ' '
ATTRIBUTE = ' '

def print_footer(stdscr, message):
    stdscr.move(max_y - 1, 0)
    stdscr.clrtoeol()
    stdscr.addstr(max_y - 1, 0, message)
    stdscr.refresh()


def init(stdscr):
    global max_y
    global max_x
    max_y = stdscr.getmaxyx()[0]
    max_x = stdscr.getmaxyx()[1]
    print_footer(stdscr, 'Initializting contracts...')
    stdscr.refresh()
    objectcache.CachedDict()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

def display_price(stdscr):
    global gold_p
    global silver_p
    print_footer(stdscr, 'Displaying price...')
    
    while True:
        try:
            gold_p_n = data.get_gold()
            silver_p_n = data.get_silver()


            if gold_p_n > gold_p:
                stdscr.addstr(0, 0, 'Gold: {}'.format(gold_p_n), curses.color_pair(2))
            elif gold_p_n < gold_p:
                stdscr.addstr(0, 0, 'Gold: {}'.format(gold_p_n), curses.color_pair(1))
            if silver_p_n > silver_p:
                stdscr.addstr(0, 40, 'Silver: {}'.format(silver_p_n), curses.color_pair(2))
            elif silver_p_n < silver_p:
                stdscr.addstr(0, 40, 'Silver: {}'.format(silver_p_n), curses.color_pair(1))
            stdscr.refresh()
            time.sleep(0.2)
            stdscr.addstr(0, 0, 'Gold: {}'.format(gold_p_n), curses.color_pair(0))
            stdscr.addstr(0, 40, 'Silver: {}'.format(silver_p_n), curses.color_pair(0))
                
            gold_p = gold_p_n
            silver_p = silver_p_n
            stdscr.refresh()
            time.sleep(2.0)
        except:
            pass

def display_orderbook(stdscr, instr, att):
    stdscr.move(2,0)
    stdscr.clrtobot()
    contracts = objectcache.CachedDict().Traded[instr][att]
    i = 3
    for c in contracts:
        stdscr.addstr(i, 0, str(i-2) + ' ' +c.name)
        i = i + 1

def display_booknumber(stdscr, instr, att, n):
    contracts = objectcache.CachedDict().Traded[instr][att]
    try:
        c = contracts[n-1]
    except:
        print_footer(stdscr, 'Index out of change')
    stdscr.move(2,0)
    stdscr.clrtobot()
    stdscr.addstr(2,0, c.name)
    j = httphandler.getContractOrders(c.conID)

    stdscr.addstr(4, 15, '#')
    stdscr.addstr(4, 35, '#')
    stdscr.addstr(4, 20, 'Bid')
    stdscr.addstr(4, 40, 'Ask')
    i = 0
    for o in j['Bids']:
        stdscr.addstr(i+6, 15, str(o['Quantity']))
        stdscr.addstr(i+6, 20,"{0:.2f}".format(o['Price']/100000.00))
        i = i + 1
    i = 0
    for o in j['Asks']:
        stdscr.addstr(i+6, 35, str(o['Quantity']))
        stdscr.addstr(i+6, 40,"{0:.2f}".format(o['Price']/100000.00))
        i = i + 1

    stdscr.refresh()


def event_key(stdscr):
    global STATE
    global INSTRUMENT
    global ATTRIBUTE
    while True:
        try:
            c = stdscr.getch()
            if c == ord('q'):
                STATE = 'q'
            elif c == ord('p'):
                STATE = 'p'
                thread.start_new_thread(display_price, (stdscr,))
            elif c == ord('o'):
                STATE = 'o'
                print_footer(stdscr, '1.Gold End 2.Silver End 3.Gold Above 4.Silver Above')
                c = stdscr.getch()
                if c == ord('1'):
                    display_orderbook(stdscr, 'Gold', 'End')
                    INSTRUMENT = 'Gold'
                    ATTRIBUTE = 'End'
                elif c == ord('2'):
                    display_orderbook(stdscr, 'Silver', 'End')
                    INSTRUMENT = 'Silver'
                    ATTRIBUTE = 'End'
                elif c == ord('3'):
                    display_orderbook(stdscr, 'Gold', 'Max')
                    INSTRUMENT = 'Gold'
                    ATTRIBUTE = 'Max'
                elif c == ord('4'):
                    display_orderbook(stdscr, 'Silver', 'Max')
                    INSTRUMENT = 'Silver'
                    ATTRIBUTE = 'Max'
                else:
                    print_footer(stdscr, 'Error input')
                stdscr.refresh()
            elif c >= ord('1') and c <= ord('9'):
                if STATE == 'o':
                    display_booknumber(stdscr, INSTRUMENT, ATTRIBUTE, c - ord('1') + 1)
            elif c == ord('w'):
                print_footer(stdscr, 'sup')
            else:
                print_footer(stdscr, str(c))
        except:
            pass
        
def main(stdscr):
    global STATE
    init(stdscr)
    stdscr.clear()
    thread.start_new_thread(event_key, (stdscr,))
    while True:
        if STATE == 'q':
            break
        time.sleep(0.2)

if __name__ == '__main__':
    wrapper(main)
