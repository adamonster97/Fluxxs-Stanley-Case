import pandas as pd
import numpy as np
from ir_model import *
from price import *

#cur Parameters
i = 0.005
phi0 = 0.05


def calibrateParam(a0,phi0,N):
    iter = 0
    target = priceCapletBlack()

    f = lambda i: priceCaplet(genModel(i,phi0)[1]).rename(i)
    x = pd.DataFrame([f(i) for i in np.arange(0.005,.1,0.005)])

    while iter < N:

        iter += 1
