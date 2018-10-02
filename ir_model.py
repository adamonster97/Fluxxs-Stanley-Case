import pandas as pd
import numpy as np
import ir_param

NUM_PATHS = 1000
NUM_PERIODS = 7

def genModel(NUM_PATHS,NUM_PERIODS, s = 0):

    factor_1 = np.random.normal(size=(NUM_PATHS,NUM_PERIODS))
    factor_2 = np.random.normal(size=(NUM_PATHS,NUM_PERIODS))

    bondPrices = pd.DataFrame(index=range(NUM_PATHS))

    for T in np.arange(0.25,NUM_PATHS/2+0.001,0.25):
        for t in np.arange(0,T+0.001,0.25):
            tStr = "%.2f_%.2f" % (t, T)
            if(t == T):
                bondPrices[tStr] = 1
            elif(t == 0):
                bondPrices[tStr] = np.exp(-1 * param.loc[t,"Zero_YTM"] * t)
            else:



    YTM = pd.DataFrame()
