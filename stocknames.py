#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import tushare as ts
class StockNames:
	def __init__(self):
		self.load_db()

	def load_db(self):
		try:
			f = open('names.json', 'r')
			self.names = json.load(f)
		except:
			self.build_db()
			
	def build_db(self):
		df = ts.get_today_all()
		rows, cols = df.shape
		self.names = dict()
		for i in range(rows):
			self.names[df.ix[i,'code']] = df.ix[i,'name']
	
		with open('names.json', 'w') as f:
			json.dump(self.names, f)
	
	def print_all(self):
		count = 0
		for code, name in self.names.iteritems():
			print code, name
			count += 1
		print "total", count
	
	def filelist(self,f):
		for code in self.names:
			f.write(code+'\n')
					
		
	def find(self, code):
		if code in self.names:
			return self.names[code]
		else:
			return u"Not find"
		
if __name__ == "__main__":
	names = StockNames()
	
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', '-f', help='export codes to a file', type=str)
	parser.add_argument('--show', '-s', help='show codes, names on screen', action='store_true')
	args = parser.parse_args()
	
	if args.file:
		with open(args.file,'w') as fout:
			names.filelist(fout)
			fout.close()
		
	if args.show:
		names.print_all()
		
