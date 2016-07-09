
class Analyzer:
	def __init__(self):
		from stockhistory import StockHist
		self.hist = StockHist()
		
	def compute(self, db):
		import stocknames
		names = stocknames.StockNames()
		for code, diary in db.iteritems():		
			name = names.find(code)
			print name, code
			for date,val in sorted(diary.items(), reverse = True):
				print date, val[1]/10.0**8-val[0]/10.0**8, self.hist.find(code, date)

if __name__=="__main__":
	with open('new.json','r') as f_db:
		import json
		a = Analyzer()
		a.compute(json.load(f_db))
