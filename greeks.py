import pandas as pd
import numpy as np
from ir_model import *
from product import *

(bondPrc, YTM) = genModel(0.2,0.05)

"""
Calculate the Greeks
"""

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

def perterbDelta(bondPrc,p = 0.0001):
    return yieldToPrice(priceToYield(bondPrc) + p)

def Vega(bondPrc,rise_ki,flat_ki,p = 0.01):
    productPriceAll(bondPrc,priceToYTM(bondPrc),)
    newPrc = perterbVega(bondPrc, p)
    newYTM = priceToYTM(newPrc)
    productPriceAll(newPrc,newYTM,rise_ki,flat_ki)

def Delta(bondPrc,rise_ki,flat_ki,p = 0.0001):
    productPriceAll(bondPrc,priceToYTM(bondPrc),)
    newPrc = perterbDelta(bondPrc, p)
    newYTM = priceToYTM(newPrc)
    productPriceAll(newPrc,newYTM,rise_ki,flat_ki)
