import pandas as pd
import numpy as np
import scipy.optimize as opt
from ir_model import *
from price import *

phi0 = 1
a0 = 0.2
t = 0.25

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
        N = 25

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
                print("C")
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
    A1 = calibrate(phi0 = 0.1, a0 = 1)
    A2 = calibrate(phi0 = 0.2, a0 = 1)
    A3 = calibrate(phi0 = 0.5, a0 = 1)
    A4 = calibrate(phi0 = 1, a0 = 1)
    A5 = calibrate(phi0 = 2, a0 = 1)
