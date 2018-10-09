import pandas as pd
import numpy as np
import scipy.optimize as opt
from ir_model import *
from correlation_calc import *
from price import *

# phi0 = 1
# a0 = 0.2
# t = 0.25

def calibrate(phi0 = 0.05, a0 = 0.2):
    param = getParam()
    targetP = priceCapletBlack()
    targetC = 0.81

    def getPFunct(t,a,phi):
        def price(a_t = 0.05):
            aN = a.set_value(t,a_t)
            ret = (priceCaplet(genModel(aN,phi)[1],t) - targetP.loc[t])
            # print("T = %f, ret = %f, a_t = %f" % (t,ret,a_t))
            return ret
        return price

    finA = pd.Series(np.NAN,index=param.index)
    for t in param.index[:-1]:
        curA = finA.copy()
        curA.fillna(a0,inplace=True)

        f = getPFunct(t,curA,phi0)

        tol = 1e-08
        i = 0
        N = 50

        a = 0
        fa = f(a)
        b = 2 * a0
        fb = f(b)
        p =  (a + b)/2
        fp = f(p)
        if abs(fa) < tol:
            continue # (a,fa)
        elif abs(fb) < tol:
            continue # (b,fb):

        while i < N:
            if abs(fp) < tol:
                #print("C")
                continue # (p,fp)
            if fp > 0:
                b = p
            else:
                a = p
            p = (a + b)/2
            fp = f(p)

            print("%d    P = %f, fp = %f" % (i,p,fp))
            i += 1

        print("BREAK")
        finA[t] = p
    return finA

if __name__ == "__main__":

  phi0 = 0.005
  curAs = calibrate(phi0=phi0, a0=1)

  print("Phi: %0.2f" % phi0)
  (bondPrices, YTM) = genModel(list(curAs.values), phi0)
  corr = get_3mon_1yr_corr(bondPrices)
  print("Correlation: %0.8f" % corr)
  print("---------------------")

  #from graphics import *
  #plot(YTM)
