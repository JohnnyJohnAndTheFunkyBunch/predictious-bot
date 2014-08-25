import math
import time


days_year = 252 # or 252, 365
time_year = days_year * 24 * 60 * 60
time_year = float(time_year)
# time_open = 52200.00
# time_close = 75600.00

def get_tenor(time_close):
    return (time_close - time.time())/time_year

########################## Finance Stuff ##########################

def value(S, K, r, sigma, tenor, isCall):
    d1 = dOne(S, K, r, sigma, tenor)
    d2 = d1 - sigma * math.sqrt(tenor)

    if isCall:
        val = math.exp(-r * tenor) * phi(d2)
    else:
        val = math.exp(-r * tenor) * phi(-d2)
    if val > 1:
        val = 1
    if val < 0:
        val = 0
    return val

def dOne(S, K, r, sigma, tenor):
    return (math.log(S / K) + (r + 0.5 * sigma * sigma) * tenor) / (sigma * math.sqrt(tenor))

def phi(x):
    'Cumulative distribution function for the standard normal distribution'
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def up_and_in_cash_at_hit_or_nothing(S, H, r, sigma, tenor):
    # S: Asset price
    # H: Barrier price
    # r: risk free rate ( 0? or make it 0.02? doesn't matter too much)
    # K: payoff
    # sigma: annualized vol
    # tenor: time to maturity in years
    # CND: cumulative normal distribution

    K = 1 # normalized, or 10 mBTC
    v = sigma
    mu = (0 - v*v/2)/(v * v) # -1/2
    eta = -1
    l = math.sqrt(mu*mu + 2 * r/(v*v))
    Z = math.log(H/S)/(v * math.sqrt(tenor)) + l * v * math.sqrt(tenor)
    a5 = (K * ((H/S)**(mu + l) * phi(eta * Z) + ((H/S)**(mu - l)) * \
               phi(eta * Z - 2 * eta * l * v * math.sqrt(tenor))))
    if a5 > 1:
        a5 = 1
    if a5 < 0:
        a5 = 0
    return a5 

if __name__ == "__main__":
    previous = time.clock()
    print str(up_and_in_cash_at_hit_or_nothing(1400, 1500.0, 0.0, 0.2, 0.3))
    print 'Time: ' + str(time.clock() - previous)
    previous = time.clock()
    print str(value(1400, 1500.0, 0.0, 0.2, 0.3, True))
    print 'Time: ' + str(time.clock() - previous)
    
