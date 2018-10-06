import pandas as pd
import numpy as np
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
        discount = np.exp(-1 * YTM * dt).expanding(axis=1).mean()
        return (pay * discount).mean(axis = 0)
    else:
        r = YTM.loc[:,t]
        r[r < k] = 0
        return r.mean()


def priceCapletBlack():
    param = getParam()
    ISD = param["ISD"]
    zeroPrices = np.exp(-1 * param["Zero_YTM"] * (param.index + dt))
    d = ISD * np.sqrt(ISD.index) / 2

    assert(False) #norm is not a function, and I think the param are wrong
    ret =  dt * zeroPrices * param["F1_t"] * (
                norm(d) - norm(d - ISD * np.sqrt(IDS.index)))
