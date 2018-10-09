from hedge import *

def summary(bondPrc, duration, spread):

	rows = [0, .25, .5, 1]

	res = pd.DataFrame(0, index = rows, columns = ['Average', 'Vol'])

	for i in range(len(rows)):
		if spread == True:
			prc = bondPrc[(rows[i], rows[i]+duration)]

			rate = prc.apply(lambda x: -math.log(x)/duration)

			res.iloc[i,0] = rate.mean()
			res.iloc[i, 1] = rate.std()

		else:
			sprd = bondPrc[(rows[i],rows[i]+1)] - bondPrc[(rows[i],rows[i]+.25)]
			res.iloc[i,0] = sprd.mean()
			res.iloc[i,1] = sprd.std()

	return res

def rates_sum():

	r3_sum = summary(bondPrc, 0.25, False)
	r1_sum = summary(bondPrc, 1, False)

	spread_sum = summary(bondPrc, 1, True)

	return (r3_sum, r1_sum, spread_sum)

(r3_sum, r1_sum, spread_sum) = rates_sum()



