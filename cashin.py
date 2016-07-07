# -*- coding: utf-8 -*- 
import tushare as ts

def day_cashin(df):
	rows, cols = df.shape
	# too few rows, no available data in this day
	if rows<100:
		return None
	total_cashin = 0.0
	total_volume = 0.0
	for i in range(rows):
		sig = 0
		if df.ix[i,'type']=='\xe5\x8d\x96\xe7\x9b\x98': #　selling
			sig = -1
		elif df.ix[i, 'type']=='\xe4\xb9\xb0\xe7\x9b\x98': # buying
			sig = 1
		moment_cashin = sig*df.ix[i,'amount']
		total_volume += sig*100.0*df.ix[i, 'volume']
		total_cashin += moment_cashin
	return total_cashin, total_volume, df.ix[0,'price']
	

def recent_cashin(stock, days=30):
	from datetime import date, datetime, timedelta
	today = date(2016,7,7)
	cashin = 0
	volume = 0
	for i in range(30):
		d = today - timedelta(days=i)
		df = ts.get_tick_data(stock, date=d)
		ret = day_cashin(df)
		if ret!=None:
			volume += ret[1]
			cashin += ret[0]
			print d, ret[0]/100000000.0, ret[2] # chinese Yi
	print 'total_cashin', cashin/100000000.0
	
if __name__=="__main__":
	f = open('stocks.dat', 'r')
	for line in f:
		print line
		recent_cashin(line.rstrip())

	

