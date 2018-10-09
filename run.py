import pandas as pd
import numpy as np
import scipy.optimize as opt
from ir_model import *
from ir_calib import *
from correlation_calc import *
from price import *
from product import *
from hedge import *
from greeks import *

def summary(bondPrice, duration, spread):

  rows = [0, .25, .5, 1]

  res = pd.DataFrame(0, index = rows, columns = ['Average', 'Vol'])

  for i in range(len(rows)):
    if spread == False:
      prc = bondPrice[(rows[i], rows[i]+duration)]

      rate = prc.apply(lambda x: -math.log(x)/duration)

      res.iloc[i,0] = rate.mean()
      res.iloc[i, 1] = rate.std()

    else:
      sprd = bondPrice[(rows[i],rows[i]+1)] - bondPrice[(rows[i],rows[i]+.25)]
      res.iloc[i,0] = sprd.mean()
      res.iloc[i,1] = sprd.std()

  return res

def rates_sum(bondPrices):

  r3_sum = summary(bondPrices, 0.25, False)
  r1_sum = summary(bondPrices, 1, False)

  spread_sum = summary(bondPrices, 1, True)

  return (r3_sum, r1_sum, spread_sum)

if __name__ == "__main__":
  param = getParam()
  # Calibrate Model
  phi0 = 0.005
  curAs = calibrate(phi0=phi0, a0=1)
  curAs.to_pickle("calib.pkl")
  # curAs = pd.read_pickle("calib.pkl")
  (bondPrices, YTM) = genModel(list(curAs.values), phi0)

  # Check Correlation
  # corr = get_3mon_1yr_corr(bondPrices)
  # print("Correlation: %0.8f" % corr)


  NOTIONAL = 10000000
  cur_3m = .052
  cur_1y = .0572
  (r1, r3) = get_fut_spot(bondPrices)

  rise_ki = 0.00
  flat_ki = 0.0026
  # (payoffs, l1, l3) = get_payoff(r1,r3, rise_ki, flat_ki)
  #
  # price = payoffs.mean()*np.exp(-cur_1y)*NOTIONAL
  # print("Price: %0.10f" % price)
  #
  # max_payoff = max(payoffs)
  # max_price = max_payoff*np.exp(-cur_1y)*NOTIONAL
  # print('Bull PV: %.10f' % max_price)

  Vega(bondPrices,0,0.0026).mean()*1e6
  Delta(bondPrices,0,0.0026).mean()*1e6
  #
  VegaCovered(bondPrices,0,0.0026).mean() * 1e6
  DeltaCovered(bondPrices,0,0.0026,0.0001).mean() * 1e6

  # from mpl_toolkits.mplot3d import Axes3D
  # fig, ax = plt.subplots(nrows = 1, ncols = 1)

  # xs = np.arange(0,0.004,0.0001)
  # #ys = np.arange(0,0.05,0.001)

  # xvals = list()
  # yvals = list()

  # for x in xs:
  #   xvals.append(x*10000)
  #   payoffs = get_payoff(r1,r3, 0, x)
  #   price = payoffs.mean()*np.exp(-cur_1y)*NOTIONAL
  #   yvals.append(price)

  # ax.plot(xvals, yvals)
  # plt.title("Knock-In Level vs. KNIFE")
  # plt.xlabel('Flattener Knock-In Level (bps)')
  # plt.ylabel('Premium (USD on \$1M Notional)')
  # plt.show()

  # (r3_sum, r1_sum, spread_sum) = rates_sum(bondPrices)
  # payout = VaR(bondPrices,rise_ki,flat_ki)



unhedged = VaR(bondPrices,rise_ki,flat_ki) * 1e6
hedged = VaRHedged(bondPrices,rise_ki,flat_ki) * 1e6
plt.hist(unhedged[unhedged < 0],50,color="green")
plt.hist(hedged[hedged < 0],50,color="orange")
plt.show()

plt.hist(hedged,50,color="orange")
plt.hist(unhedged,50,color="green")
plt.show()


hedged.quantile([0.05,0.5,0.95])
