import pandas as pd
import numpy as np
from ir_model import *

'''
Not sure if I undertand this correctly
so the code is not very dynamic...
  ie. I could loop through the periods in the 
  first two functions
'''

# Calculate absolute changes in 3mon forward spot rates
def get_three_mon_changes(bondPrices):
  period = 0.25
  c1 = get_spots(bondPrices[(0.25, 0.5)],period) - get_spots(bondPrices[(0, 0.25)], period)
  c2 = get_spots(bondPrices[(0.5, 0.75)],period) - get_spots(bondPrices[(0.25, 0.5)], period)
  c3 = get_spots(bondPrices[(0.75, 1)],period) - get_spots(bondPrices[(0.5, 0.75)], period)
  c4 = get_spots(bondPrices[(1, 1.25)],period) - get_spots(bondPrices[(0.75, 1)], period)
  return pd.concat([c1, c2, c3, c4], axis = 1)

# Calculate absolute changes in 1yr forward spot rates
def get_one_yr_changes(bondPrices):
  period = 1
  c1 = get_spots(bondPrices[(0.25, 1.25)],period) - get_spots(bondPrices[(0, 1)], period)
  c2 = get_spots(bondPrices[(0.5, 1.5)],period) - get_spots(bondPrices[(0.25, 1.25)], period)
  c3 = get_spots(bondPrices[(0.75, 1.75)],period) - get_spots(bondPrices[(0.5, 1.5)], period)
  c4 = get_spots(bondPrices[(1, 2)],period) - get_spots(bondPrices[(0.75, 1.75)], period)
  return pd.concat([c1, c2, c3, c4], axis = 1)

# Convert bond prices to forward spot rate, given period
def get_spots(bond_prices, period):
  # Convert bond prices to FR spot rates
  # period 0.25 = 3 months
  return (-1/period)*np.log(bond_prices)

# Returns mean correlation between all paths (rows) of two dfs
def get_correlation(df1, df2):
  # Calculate correlation between each path
  #corrs = [df1.iloc[x,:].corr(df2.iloc[x,:]) for x in range(0, len(df1))]
  return df1.unstack().corr(df2.unstack())

# Returns the mean correlation between the quarterly changes in 
# the 1yr and 3mon rates
def get_3mon_1yr_corr(bondPrices):
  three_mon = get_three_mon_changes(bondPrices)
  one_yr = get_one_yr_changes(bondPrices)
  return get_correlation(three_mon, one_yr)


if __name__ == "__main__":
  (bondPrices,YTM) = genModel(1,0)
  corr = get_3mon_1yr_corr(bondPrices)
  print("Correlation: %0.4f" % corr)

