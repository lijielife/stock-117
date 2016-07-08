### Framework of the stock selector
1. 资金流入/流出：在一段时间内，资金流入，股价可能上涨；资金流出，股价可能下跌。
计算方式，当日成交： 对每笔进行计算，买入/卖出：　(+/-)价格×成交量
2. 对资金流入、流出量进行分析，做　时间－流入量　曲线，作为参考依据。
3. stockdict.json　用于存储一个关于stock的字典，而每一个条目又是关于时间的
4. 加入命令行工具，https://docs.python.org/2/howto/argparse.html
