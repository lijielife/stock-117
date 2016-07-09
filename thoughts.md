### Framework of the stock selector
1. 资金流入/流出：在一段时间内，资金流入，股价可能上涨；资金流出，股价可能下跌。
计算方式，当日成交： 对每笔进行计算，买入/卖出：　(+/-)价格×成交量
2. 对资金流入、流出量进行分析，做　时间－流入量　曲线，作为参考依据, 应该包含：价格、现金流量、交易量。
4. 加入命令行工具，https://docs.python.org/2/howto/argparse.html
5. 存储每天的dataframe，以利后续计算，近三年ｋ线图，hist.json, 两周内大单资金流量，all_sina.json
6. 获取所有股票对应名称，存储本地，查找工具: stocknames.py, names.json, all.dat
7. dataframe.index dataframe.columns dataframe.values dataframe.ix[...]
8. useful answer: http://stackoverflow.com/questions/3371136/revert-the-no-site-packages-option-with-virtualenv
9. 先利用ｋ线图数据，得到开盘日，再从每个开盘日计算现金流量。

