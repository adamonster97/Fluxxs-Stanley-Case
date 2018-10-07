import pandas as pd
import math
import numpy as np
from ir_model import *

(bondPrc, YTM) = genModel()

NOTIONAL = 1000000

cur_3m = .052
cur_1y = .0572

def get_fut_spot(bondPrc):
	p1 = bondPrc[(1,2)]
	p3 = bondPrc[(1,1.25)]

	r1 = p1.apply(lambda x: -math.log(x))
	r3 = p3.apply(lambda x: -math.log(x)/.25)

	return (r1, r3)

(r1, r3) = get_fut_spot(bondPrc)

def get_payoff(r1, r3):
	delta_1y = r1 - cur_1y
	delta_3m = r3 - cur_3m

	knockin_level = [0, .1]

	l1 = pd.DataFrame(0, index = r1.index.get_values(), columns = knockin_level)

	l3 = delta_3m.apply(lambda x: max(0, x))

	for i in range(len(knockin_level)):
		k = delta_1y.apply(lambda x: x > knockin_level[i])
		l1.iloc[:,i] = k * delta_1y

	payoff = pd.DataFrame(0, index = r1.index.get_values(), columns = knockin_level)

	for j in range(len(knockin_level)):
		payoff.iloc[:,j] = (np.subtract(l3, l1.iloc[:,j])).apply(lambda x: max(0, x))


	return (payoff, l3 * NOTIONAL, l1 * NOTIONAL)

(p, l3, l1) = get_payoff(r1,r3)

def get_discount(YTM):
	col = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
	discount = pd.DataFrame(0, index = YTM.index.get_values(), columns = col)
	periods = YTM.shape[1]

	for i in range(periods):
		s = YTM.iloc[:,:i+1].sum(1)
		discount.iloc[:,i] = s.apply(lambda x: math.exp(-x*.25))
	return discount

d = get_discount(YTM)

def price_option(payoff, discount):
	discount_fac = discount.iloc[:,3]

	price = payoff * discount_fac

	return price.mean()

opt_price = price_option(p, d)


