import pandas as pd
import numpy as np
import scipy.optimize as opt
from ir_model import *
from price import *

def calibrateParam(a0,phi0):
    target = priceCapletBlack()
    def price(param):
        phi = param[0]
        a = param[1:]
        (bp,YTM) = genModel(a,phi)
        return priceCaplet(YTM)

    f = lambda x: ((price(x) - target)^2).sum()
    a0.insert(0,phi0)
    return opt.minimize(f,a0)


    #f = lambda i: priceCaplet(genModel(i,phi0)[1]).rename(i)
    #x = pd.DataFrame([f(i) for i in np.arange(0.005,.1,0.005)])

if __name__ == "__main__":
    calibrateParam(a0 = [1,1,1,1,1,1,1,1,1],phi0 = 0.05)
