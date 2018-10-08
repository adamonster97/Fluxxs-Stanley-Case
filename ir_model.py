import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ir_param import *

# a = [1, 1, 1, 1, 1, 1, 1, 1, 1]
# phi = 0.05

def genModel(a = 1,phi = 0.05):
    param = getParam(a,phi)

    factor_1 = pd.DataFrame(np.random.normal(size=(NUM_PATHS,NUM_PERIODS+1)))
    #factor_1 = pd.DataFrame([[0,0.0398,  -0.4898, -0.2981, -0.0035, 0.1213,  0.1689,  -0.1743]])
    factor_1.columns = param.index

    factor_2 = pd.DataFrame(np.random.normal(size=(NUM_PATHS,NUM_PERIODS+1)))
    #factor_2 = pd.DataFrame([[0,1.8266,  0.1911,  0.1370,  0.1764,  0.2251,  0.7992,  -1.2849]])
    factor_2.columns = param.index

    bondPrices = pd.DataFrame(index=range(NUM_PATHS),
                    columns=pd.MultiIndex(levels=[[],[]],labels=[[],[]],names=["t","T"]))

    YTM = pd.DataFrame(index=range(NUM_PATHS),
                    columns=pd.MultiIndex(levels=[[],[]],labels=[[],[]],names=["t","T"]))

    for T in np.arange(dt,NUM_PERIODS*dt+err,dt):
        for t in np.arange(0,T+err,dt):
            if(t == T):
                bondPrices[(t,T)] = 1
            elif(t == 0):
                bondPrices[(t,T)] = np.exp(-1 * param.loc[T,"Zero_YTM"] * T)
            else:
                bondPrices[(t,T)] = bondPrices[(t-dt,T)]*(
                        1+YTM[t-dt]*dt +
                        param.loc[t,"s1"]*dt*np.sqrt(dt) * factor_1.loc[:,t] +
                        param.loc[t,"s2"]*dt*np.sqrt(dt) * factor_2.loc[:,t] )

            if(t == T-dt):
                YTM[t] = -np.log(bondPrices[(t,T)])

    return(bondPrices,YTM)

#(bondPrices,YTM) = genModel(1,0.05)
