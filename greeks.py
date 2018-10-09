import pandas as pd
import numpy as np
from ir_model import *

# (bondPrc, YTM) = genModel(0.2,0.05)

"""
Calculate the Greeks
"""

def priceToYield(bondPrc):
    ret = pd.DataFrame(index = bondPrc.index, columns = bondPrc.columns)
    for ((t,T),curP) in bondPrc.iteritems():
        if (t == T):
            ret[(t,T)] = 0
        else:
            ret[(t,T)] = -np.log(curP) / (T-t)

    return ret

def yieldToPrice(yields):
    ret = pd.DataFrame(index = yields.index, columns = yields.columns)
    for ((t,T),curY) in yields.iteritems():
        if (t == T):
            ret[(t,T)] = 1
        else:
            ret[(t,T)] = np.exp(-1 * curY * (T-t))

    return ret

def perterbVega(bondPrc,p = 0.01):
    ret = pd.DataFrame(index = bondPrc.index, columns = bondPrc.columns)
    ylds = priceToYield(bondPrc)
    for ((t,T),Y) in ylds.iteritems():
        mu = Y.mean()
        sd = Y.std()
        cur = (Y - mu)/sd
        cur *= 1 + p
        ret[(t,T)] = (cur * sd) + mu

    return yieldToPrice(ret)


def delta(bondPrc,p = 0.0001):
    return yieldToPrice(priceToYield(bondPrc) + p)
