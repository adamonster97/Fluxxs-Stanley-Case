import pandas as pd
import math
import numpy as np
from product import *

## long interest rate options on 1y and 3m tsy rates

def price_hedge(r1, r3, discount, l1, l3):
	E_3m_payoff = l3.mean()
	E_1y_payoff = l1.mean()

	hedge_ratio = E_3m_payoff/E_1y_payoff * 6.5

	payoff_3m = (r3 - cur_3m).apply(lambda x: max(x, 0))
	payoff_1y = (r1 - cur_1y).apply(lambda x: max(x, 0))

	discount_fac = discount.iloc[:,3]

	total_payoff = payoff_3m * hedge_ratio + payoff_1y

	price = total_payoff* discount_fac

	return (total_payoff, price)


def hedgeAll(bondPrc,rise_ki,flat_ki):
	(r1, r3) = get_fut_spot(bondPrc)
	(payoffs, l1, l3) = get_payoff(r1,r3, rise_ki, flat_ki)

	payoff, price = price_hedge(r1,r3,get_discount(priceToYTM(bondPrc)), l1, l3)

	return price
