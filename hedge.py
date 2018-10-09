import pandas as pd
import math
import numpy as np
from product import *

## long interest rate options on 1y and 3m tsy rates

E_3m_payoff = sum(l3[l3>0])/NUM_PATHS
E_1y_payoff1 = sum(l1.iloc[:,0])/NUM_PATHS
E_1y_payoff2 = sum(l1.iloc[:,1])/NUM_PATHS

hedge_ratio1 = E_3m_payoff/E_1y_payoff1
hedge_ratio2 = E_3m_payoff/E_1y_payoff2

def price_hedge(r1, r3, discount):
	payoff_3m = (r3 - cur_3m).apply(lambda x: max(x, 0))
	payoff_1y = (r1 - cur_1y).apply(lambda x: max(x, 0))

	discount_fac = discount.iloc[:,3]

	total_payoff1 = payoff_3m * hedge_ratio1 + payoff_1y
	total_payoff2 = payoff_3m * hedge_ratio2 + payoff_1y

	price = pd.DataFrame(0, index = r1.index.get_values(), columns = ['knockin1','knockin2'])

	price1 = total_payoff1 * discount_fac
	price2 = total_payoff2 * discount_fac

	return (price1, price2)

print(price_hedge(r1, r3, d))


