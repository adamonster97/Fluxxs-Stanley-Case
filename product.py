import pandas as pd
import math
import numpy as np
from ir_model import *

# (bondPrc, YTM) = genModel()

NOTIONAL = 1000000
cur_3m = .052
cur_1y = .0572

# spot 1y from now
def get_fut_spot(bondPrc):
	p1 = bondPrc[(1.0,2.0)]
	p3 = bondPrc[(1.0,1.25)]

	r1 = p1.apply(lambda x: -math.log(x))
	r3 = p3.apply(lambda x: -math.log(x)/.25)

	return (r1, r3)


def get_payoff(r1, r3, rise_ki, flat_ki):
	delta_1y = r1 - cur_1y
	delta_3m = r3 - cur_3m

	l1 = delta_1y.apply(lambda x: max(x, 0))
	l3 = delta_3m.apply(lambda x: max(x, 0))

	payoff = (l3 - l1).apply(lambda x: max(x, 0))

	# Rise KNOCK-IN
	k = delta_1y.apply(lambda x: x > rise_ki)
	payoff = k * payoff

	# Flatten KNOCK-IN
	new_spread = r1 - r3
	k = new_spread.apply(lambda x: x < flat_ki)
	payoff = k * payoff

	# payoff = pd.DataFrame(0, index = r1.index.get_values(), columns = knockin_level)
	# payoff.iloc[:,j] = (np.subtract(l3, l1.iloc[:,j])).apply(lambda x: max(0, x))

	return (payoff, l1,l3)

def get_discount(YTM):
	col = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
	discount = pd.DataFrame(0, index = YTM.index.get_values(), columns = col)
	periods = YTM.shape[1]

	for i in range(periods):
		s = YTM.iloc[:,:i+1].sum(1)
		discount.iloc[:,i] = s.apply(lambda x: math.exp(-x*.25))
	return discount

def price_option(payoff, discount):
	discount_fac = discount.iloc[:,3]

	price = payoff.multiply(discount_fac)

	return price

def productPriceAll(bondPrc,YTM,rise_ki,flat_ki):
	(r1, r3) = get_fut_spot(bondPrc)
	(p,l1,l3) = get_payoff(r1,r3,rise_ki,flat_ki)
	d = get_discount(YTM)
	opt_price = price_option(p, d)
	return opt_price
