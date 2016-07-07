# -*- coding: utf-8 -*- 
import tushare as ts
import sys,json

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
	# calender is each day's cashin, volume, price
	calender = dict()
	for i in range(30):
		d = str(today - timedelta(days=i))
		df = ts.get_tick_data(stock, date=d)
		ret = day_cashin(df)
		if ret!=None:
			calender[d] = (ret[0], ret[1], ret[2])
		else:
			calender[d] = (0, 0, 0)
		print calender[d]
	return calender

def compute_cash(stockdict):
	for stock, diary in stockdict.iteritems():
		total_cashin = 0
		for day in diary:
			cash, volume, price = diary[day]
			total_cashin += cash
		df = ts.get_realtime_quotes(stock)
		name = df.ix[0,'name']
		print stock, name, total_cashin/100000000.0
		

#stocks is a list of stock codes, build a brand new dictionary
def build_by_stocks(stocks):
	stockdict = dict()
	for stock in stocks:
		print stock
		stockdict[stock] = recent_cashin(stock)
			
	with open('stockdict.json', 'w') as f:
		json.dump(stockdict, f)
		
#stocks is a list of stock codes, maybe contain new codes
def update_by_stocks(stockdict, stocks):
	for s in stocks:
		if not s in stockdict:
			print 'to be updated:', s
			stockdict[s] = recent_cashin(s)
	
	with open('stockdict.json', 'w') as f:
		json.dump(stockdict, f)

if __name__=="__main__":
	if (len(sys.argv)>1):
		# build data
		if sys.argv[1]=='b':
			with open('stocks.dat') as f:
				stocks = f.read().splitlines()
				build_by_stocks(stocks)
			
		# read data and compute
		elif sys.argv[1]=='c':
			with open('stockdict.json', 'r') as f:
				stockdict = json.load(f)
				compute_cash(stockdict)
				
		# update data
		elif sys.argv[1]=='u':
			with open('stocks.dat') as f1, open('stockdict.json') as f2:
				stocks = f1.read().splitlines()
				stockdict = json.load(f2)
				update_by_stocks(stockdict, stocks)
		
		# clear data, change format
		elif sys.argv[1]=='n':
			with open('stockdict.json','r+') as f:
				stockdict = json.load(f)
				for s, diary in stockdict.iteritems():
					if 'name' in diary:
						diary.pop('name', None)
			with open('stockdict.json', 'w') as f:
				json.dump(stockdict, f)	
