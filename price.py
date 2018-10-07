import pandas as pd
import numpy as np
import scipy.stats as stats
from ir_param import *

#YTM = genModel(1,0.05)[1]

def priceCaplet(YTM,t = None,k = None):
    param = getParam()
    if k is None:
        if t is None:
            k = param["F1_t"]
        else:
            k = param.loc[t,"F1_t"]

    if t is None:
        #Do I need to copy YTM?
        pay = YTM.subtract(k,level="t").copy()
        pay[pay < 0] = 0
        discount = np.exp(-1 * YTM * dt).expanding(axis=1).prod()
        return (pay * discount).mean(axis = 0)
    else:
        pay = YTM.loc[:,t] - k
        discount = np.exp(-1 * YTM.loc[:,:t] * dt).prod()
        pay[pay < 0] = 0
        return pay.mean(axis = 0)


def priceCapletBlack():
    param = getParam()
    zeroPrices = np.exp(-1 * param["Zero_YTM"] * (param.index))
    d1 = param["ISD"] * np.sqrt(param.index)/2
    d2 = d1 - param["ISD"] * np.sqrt(param.index)
    return dt * zeroPrices.shift(-1) * (
        param["F1_t"] * stats.norm.cdf(d1) -
        param["F1_t"] * stats.norm.cdf(d2))
