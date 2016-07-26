
class Analyzer:
	def __init__(self):
		pass

	def compute(self, db):
		import stocknames
		names = stocknames.StockNames()
		for code, diary in db.iteritems():		
			name = names.find(code)
			print name, code
			for date, val in sorted(diary.items(), reverse = True):
				ret, info = val#val[1]/10.0**8-val[0]/10.0**8
				print ret
				print info
			

if __name__=="__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("data", help="json formatted stock flow data to analyze", type = str)
	args = parser.parse_args()
	with open(args.data,'r') as f_db:
		import json
		a = Analyzer()
		a.compute(json.load(f_db))
