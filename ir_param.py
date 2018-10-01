import pandas as pd
import numpy as np

def s1(a):
    return phi * a

def s2(a):
    return a * (np.exp(-2 * (a.index - 0.25)) - 0.5)

phi = 0.05
param = pd.DataFrame(
             [0.0520,0.0575,0.0591,0.0601,0.0609,0.0643,0.0667,0.0642], #1 year forward rate
             [0,0.25,0.5,0.75,1,1.25,1.5,1.75], #index / year
             ["F1_t"])

param["Zero_YTM"] = param["F1_t"].expanding().apply(
    lambda x: ((1+x/4).prod() - 1) / (len(x)/4))

param["a"] = 1

param["s1"] = s1(param["a"])
param["s2"] = s2(param["a"])
