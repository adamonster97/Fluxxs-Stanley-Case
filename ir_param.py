import pandas as pd
import numpy as np

def s1(a,phi):
    return phi * a

def s2(a,phi):
    print(a.index - 0.25)
    return a * (np.exp(-2 * (a.index - 0.25)) - 0.5)


def getParam(a = 1,phi = 0.05):
    param = pd.DataFrame(
             [0.0520,0.0575,0.0591,0.0601,0.0609,0.0643,0.0667,0.0642], #1 year forward rate
             [0,0.25,0.5,0.75,1,1.25,1.5,1.75], #index / year
             ["F1_t"])

    param["Zero_YTM"] = [0.0520,0.0547500,0.0562,0.0572,0.0579,0.0590,0.0601,0.0606]
    #param["F1_t"].expanding().apply(lambda x: ((1+x/4).prod() - 1) / (len(x)/4))

    param["a"] = a

    param["s1"] = s1(param["a"],phi)
    param["s2"] = s2(param["a"],phi)

    return param
