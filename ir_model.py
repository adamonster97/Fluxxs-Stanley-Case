import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ir_param import *

NUM_PATHS = 1000
NUM_PERIODS = 7

dt = 0.25
err = 0.001

def colStr(t,T):
    return "%.2f_%.2f" % (t, T)

t = 0
T = 0.5

def genModel(a,phi):
    param = getParam(a,phi)

    factor_1 = pd.DataFrame(np.random.normal(size=(NUM_PATHS,NUM_PERIODS+1)))
    #factor_1 = pd.DataFrame([[0,0.0398,  -0.4898, -0.2981, -0.0035, 0.1213,  0.1689,  -0.1743]])
    factor_1.columns = param.index

    factor_2 = pd.DataFrame(np.random.normal(size=(NUM_PATHS,NUM_PERIODS+1)))
    #factor_2 = pd.DataFrame([[0,1.8266,  0.1911,  0.1370,  0.1764,  0.2251,  0.7992,  -1.2849]])
    factor_2.columns = param.index

    bondPrices = pd.DataFrame(index=range(NUM_PATHS))
    YTM = pd.DataFrame(index=range(NUM_PATHS))

    for T in np.arange(dt,NUM_PERIODS*dt+err,dt):
        for t in np.arange(0,T+err,dt):
            curStr = colStr(t,T)
            prevStr = colStr(t-dt, T)
            print(curStr)

            if(t == T):
                bondPrices[curStr] = 1
            elif(t == 0):
                bondPrices[curStr] = np.exp(-1 * param.loc[(T-0.25),"Zero_YTM"] * T)
            else:
                bondPrices[curStr] = bondPrices[prevStr]*(
                        1+YTM[t-dt]*dt +
                        param.loc[dt:T,"s1"].sum()*dt*np.sqrt(dt) * factor_1.loc[:,t] +
                        param.loc[dt:T-dt,"s2"].sum()*dt*np.sqrt(dt) * factor_2.loc[:,t] )

            if(t == T-dt):
                YTM[t] = -np.log(bondPrices[curStr])

    return(bondPrices,YTM)

(bondPrices,YTM) = genModel(NUM_PATHS,NUM_PERIODS)

plt.plot(YTM.transpose(),color="green")
plt.plot(YTM.mean(axis=0),linewidth=4,color="blue")
plt.show()
