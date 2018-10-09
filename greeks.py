import pandas as pd
import numpy as np
from ir_model import *
from product import *
from hedge import *

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
    oldP = productPriceAll(bondPrc,priceToYTM(bondPrc),rise_ki,flat_ki)
    newPrc = perterbVega(bondPrc, p)
    newYTM = priceToYTM(newPrc)
    newP = productPriceAll(newPrc,newYTM,rise_ki,flat_ki)
    return oldP - newP

def Delta(bondPrc,rise_ki,flat_ki,p = 0.0001):
    oldP = productPriceAll(bondPrc,priceToYTM(bondPrc),rise_ki,flat_ki)
    newPrc = perterbDelta(bondPrc, p)
    newYTM = priceToYTM(newPrc)
    newP = productPriceAll(newPrc,newYTM,rise_ki,flat_ki)
    return oldP-newP

def VegaCovered(bondPrc,rise_ki,flat_ki,p = 0.01):
    prodPriceOld = productPriceAll(bondPrc,priceToYTM(bondPrc),rise_ki,flat_ki)
    hedgePriceOld = hedgeAll(bondPrc,rise_ki,flat_ki)

    newPrc = perterbVega(bondPrc, p)
    newYTM = priceToYTM(newPrc)

    prodPriceNew = productPriceAll(newPrc,priceToYTM(newPrc),rise_ki,flat_ki)
    hedgePriceNew = hedgeAll(newPrc,rise_ki,flat_ki)

    priceChange = (hedgePriceOld - prodPriceOld) - (hedgePriceNew - prodPriceNew)
    return priceChange

def DeltaCovered(bondPrc,rise_ki,flat_ki,p = 0.0001):
    prodPriceOld = productPriceAll(bondPrc,priceToYTM(bondPrc),rise_ki,flat_ki)
    hedgePriceOld = hedgeAll(bondPrc,rise_ki,flat_ki)

    newPrc = perterbDelta(bondPrc, p)
    newYTM = priceToYTM(newPrc)

    prodPriceNew = productPriceAll(newPrc,priceToYTM(newPrc),rise_ki,flat_ki)
    hedgePriceNew = hedgeAll(newPrc,rise_ki,flat_ki)

    priceChange = (hedgePriceOld - prodPriceOld) - (hedgePriceNew - prodPriceNew)
    return priceChange


def VaRHedged(bondPrc,rise_ki,flat_ki):
    prodPayout = productPriceAll(bondPrc,priceToYTM(bondPrc),rise_ki,flat_ki)
    hedgePayout = hedgeAll(bondPrc,rise_ki,flat_ki)/10

    payout = hedgePayout - prodPayout  + 1742 * 1e-6 - hedgePayout.mean()

    return payout


def VaR(bondPrc,rise_ki,flat_ki):
    prodPayout = productPriceAll(bondPrc,priceToYTM(bondPrc),rise_ki,flat_ki)
    payout = 1742 * 1e-6 - prodPayout

    return payout
