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
	# cash, volume, price(keep 2 digits)
	return total_cashin, total_volume, "%.2f"%df.ix[0,'price']
	

def recent_cashin(stock, days=30):
	from datetime import date, datetime, timedelta
	today = date(datetime.today().year,datetime.today().month,datetime.today().day)
	cashin = 0
	volume = 0
	rows = list()
	for i in range(30):
		d = str(today - timedelta(days=i))
		df = ts.get_tick_data(stock, date=d)
		ret = day_cashin(df)
		if ret!=None:
			volume += ret[1]
			cashin += ret[0]
			row = (d, ret[0]/100000000.0, ret[1], ret[2])# chinese Yi
			rows.append(row)
			print row
		else:
			row = (d, 0, 0, 0)
			rows.append(row)
					
	print 'total_cashin', cashin/100000000.0
	return rows
	
if __name__=="__main__":
	import sys,json
	if (len(sys.argv)>1):
		if sys.argv[1]=='b':
			f = open('stocks.dat', 'r')
			stockdict = dict()
			for line in ['603818']:
				print line
				stock = line.rstrip()
				stockdict[stock] = recent_cashin(stock) 
			with open('stockdict.json', 'w') as f:
				json.dump(stockdict, f)
		else:
			with open('stockdict.json', 'r') as f:
				stockdict = json.load(f)
				for row in stockdict['603818']:
					print row
	

