#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json,time
def get_history(code):
	import tushare as ts
	df = ts.get_hist_data(code)
	diary = dict()
	for i in df.index:
		diary[i] = df.ix[i].values.tolist()
	return diary

class Watch:
	def __init__(self,jobs):
		import time
		self.total = jobs
		self.count = 0
		self.start = time.time()
		pass
		
	def tic(self):
		self.count += 1
		used_time = time.time() - self.start
		estimated_time = used_time / self.count * (self.total-self.count)
		print "{}/{}, used {}sec, estimated {}sec".format(self.count, self.total, used_time, estimated_time)


class StockHist:
	# db structure: stocks[code][dates] = ...
	def build(self):
		import json
		with open('test/all.dat','r') as f, open('hist.json','w') as f_db:
			stocks=f.read().splitlines()
			self.db = dict()
			watch = Watch(len(stocks))
			for s in stocks:
				watch.tic()
				try:
					self.db[s] = get_history(s)
				except:
					pass
			json.dump(self.db,f_db)
		pass
		
	def load(self):
		import json
		with open('hist.json','r') as f_db:
			self.db = json.load(f_db)
	
	def find(self, code, date):
		if code in self.db:
			if 	date in self.db[code]:
				return self.db[code][date]
		
	def export_valid_dates_for_code(self, code, period):
		samples = dict()
		diary = self.db[code]
		top = sorted(diary.items(), reverse=True)[:period]
		for key, val in top:
			samples[key] = val
		return samples
		
	def export_valid_dates_for_all(self, period):
		samples = dict()
		watch = Watch( len(self.db) )	
		for s in self.db:
			watch.tic()
			samples[s] = self.export_valid_dates_for_code(s, period)
		return samples
	
	def __init__(self):
		try:
			self.load()
		except:
			self.build()
		pass
				
if __name__=='__main__':
	shist = StockHist()
	samples = shist.export_valid_dates_for_all(30)
	import json
	with open('export.json','w') as f_s:
		json.dump(samples, f_s)

