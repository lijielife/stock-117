#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from datetime import date, datetime, timedelta
def today_date():
	return date(datetime.today().year,datetime.today().month,datetime.today().day)

def day_flow_conditions(code, date):
	import tushare as ts
	sell_amount = 0
	buy_amount = 0
	sell_volume = 0
	buy_volume = 0
	df = ts.get_tick_data(code, date = date)	
	if hasattr(df,'shape'):
		rows, cols = df.shape
		for i in range(rows):
			if df.ix[i,'amount']>10**6:
				if df.ix[i,'type']=='\xe5\x8d\x96\xe7\x9b\x98': #　selling
					sell_amount += df.ix[i,'amount']
					sell_volume += df.ix[i,'volume']
				elif df.ix[i, 'type']=='\xe4\xb9\xb0\xe7\x9b\x98': # buying
					buy_amount += df.ix[i,'amount']
					buy_volume += df.ix[i,'volume']
				else:
					continue
	return (sell_amount, buy_amount, sell_volume, buy_volume)
		
def compute_cash(stockdict, today, period):
	import stocknames
	names = stocknames.StockNames()
	for stock,diary in stockdict.iteritems():
		total_cashin = 0		
		detail_txt = ""
		for i in range(period):
			day = str(today - timedelta(days=i))
			if day in diary:
				cash, volume, price = diary[day]
				total_cashin += cash
		import math
		if abs(total_cashin/10**8)>3:
			print stock, names.find(stock), total_cashin/10**8
			for i in range(period):
				day = str(today - timedelta(days=i))
				if day in diary:
					cash, volume, price = diary[day]
					if price > 0.1:
						print "{}\t{}\t{}".format(day, cash/10**8, price)
		
#stocks is a list of stock codes, build a brand new dictionary
def build_by_stocks(stocks, days, source):
	stockdict = dict()
	from stockhistory import Watch
	import tushare as ts
	watch = Watch(len(stocks))
	for stock in stocks:
		df = ts.get_hist_data(stock)
		stockdict[stock] = dict()
		for d in df.index[:days]:
			try:
				stockdict[stock][d] = day_flow_conditions(stock, date = d)
			except:
				pass
		watch.tic()
	return stockdict
		
#stocks is a list of stock codes, maybe contain new codes
def update_by_stocks(stockdict, stocks):
	for s in stocks:
		if not s in stockdict:
			print 'to be updated:', s
			stockdict[s] = recent_cashin(s)
	return stockdict

def update_by_dates(db, period, source):
	today = today_date()
	for stock,diary in db.iteritems():
		# update without today, to avoid missing data
		for i in range(1,period):
			day = str(today - timedelta(days=i))
			if not day in diary:
				diary[day] = day_flow(stock, day, source = source)
				print stock, day, diary[day]
	return db

def update_today(db, source):
	for stock, diary in db.iteritems():
		today = today_date()
		diary[today] = day_flow(stock, today, source)
		flow, vol, price = diary[today]
		print stock, flow/100000000.0, vol, price
	
if __name__=="__main__":
	import argparse,json
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	parser.add_argument("database", help="given a basic database name", type = str)
	group.add_argument("--build", "-b", help="build data from a list of stocks", type = str)
	group.add_argument("--compute", "-c", help="compute the result from data", action = "store_true")
	group.add_argument("--add", "-a", help="add data with a list of stocks", type = str)
	group.add_argument("--update", "-u", help="update the data, with the missing days, given a total amount of days", action = "store_true")
	group.add_argument("--today", "-t", help="update today's data", action = "store_true")
	group.add_argument("--new", "-n", help="change the format of database", action = "store_true")
	# type = int, choices = [1,2,3]
	parser.add_argument("--period", "-p", help="given a period of time to be considered", type = int, default = 30)
	parser.add_argument("--source", "-s", help="choose the source of the raw data, 0 for normal, 1 for sina_dd", type = int, choices=[0,1], default = 0)
	
	args = parser.parse_args()
	
	# build database from stocklist
	if args.build:
		with open(args.build) as f, open(args.database,'w') as f_db:
			stocks = f.read().splitlines()
			stockdict = build_by_stocks(stocks,days=args.period, source=args.source)
			json.dump(stockdict, f_db)
				
	# read data and compute
	if args.compute:
		with open(args.database,'r') as f_db:
			stockdict = json.load(f_db)
			compute_cash(stockdict, today=today_date(), period = args.period)
	
	# update data by dates
	if args.update:
		with open(args.database, 'r') as f_db:
			db = json.load(f_db)
			db = update_by_dates(db, period=args.period, source=args.source)
			f_db.close()
			#f_db = open(args.database, 'w')
			#json.dump(db, f_db)
	# update today
	if args.today:
		with open(args.database, 'r') as f_db:
			db = json.load(f_db)
			db = update_today(db, source=args.source)
			f_db.close()
			#f_db = open(args.database, 'w')
			#json.dump(db, f_db)
			
	# add stock data
	if args.add:
		with open(args.add) as f, open(args.database,'r') as f_db:
			stocks = f1.read().splitlines()
			db = json.load(f_db)
			db = update_by_stocks(db, stocks, period=args.period, source=args.source)
			f_db.close()
			f_db = open(args.database,'w')
			json.dump(db, f_db)
			
	# clear data, change format
	if args.new:
		with open(args.database, 'r') as f_db:
			stockdict = json.load(f_db)
			for s, diary in stockdict.iteritems():
				if 'name' in diary:
					diary.pop('name', None)
			f_db.close()
			f_db = open(args.database, 'w')
			json.dump(stockdict, f_db)
