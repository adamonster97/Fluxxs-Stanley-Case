import pandas as pd
import numpy as np

#Modeling Parameters
NUM_PATHS = 500000
NUM_PERIODS = 8
dt = 0.25
err = 0.001

def s1(a,phi):
    return phi * a

def s2(a, phi):
    return a * (np.exp(-2 * (np.arange(0,NUM_PERIODS*dt+err,dt) - 0.25)) - 0.5)

def getParam(a = 1,phi = 0.05):
    param = pd.DataFrame(
             [0.0520,0.0575,0.0591,0.0601,0.0609,0.0643,0.0667,0.0642, np.NAN], #1 year forward rate
             np.arange(0,NUM_PERIODS*dt+err,dt), #index / year
             ["F1_t"])

    param["Zero_YTM"] = [np.NAN,0.0520,0.05475,0.0562,0.0572,0.0579,0.0590,0.0601,0.0606]
    #param["F1_t"].expanding().apply(lambda x: ((1+x/4).prod() - 1) / (len(x)/4))

    param["a"] = a

    param["s1"] = s1(param["a"],phi)
    param["s2"] = s2(param["a"],phi)
    param["ISD"] =  [0,0.2416,0.2228,0.2016,0.1897,0.1757,0.1609,0.1686, np.NAN]
                            #@SN FAKE VALUE HERE 0.1652
    return param
