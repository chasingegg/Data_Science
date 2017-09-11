# -*- coding: utf-8 -*-
# Author: Chao Gao
# manipulating data

import xlrd
import xlsxwriter

data = xlrd.open_workbook(u"test.xlsx")

#得到两张表
table_sold = data.sheet_by_name(u'销售结算单')   
table_stock = data.sheet_by_name(u'进货结算单')

#获取行数和列数
sold_rows = table_sold.nrows   
sold_cols = table_sold.ncols   

#其实有多少列肯定是一样的，在这里好像有多少行也是一样的。。但还是分开写一下
stock_rows = table_stock.nrows
stock_cols = table_stock.ncols

#第一行是所有列属性的集合
colname = table_sold.row_values(0)

#这三个列属性是有用的
ID_index = colname.index(u'货品ID')
amount_index = colname.index(u'数量')
money_index = colname.index(u'金额')

#除去第一行都是有效数据，每一行作为一个元素存储到列表中，并进行排序其实如果本来就是有序且相同ID的货品都挨在一起的话排序可以省略
store_sold = [table_sold.row_values(i) for i in range(1, sold_rows)]
store_sold.sort(key = lambda x: x[ID_index])
store_stock = [table_stock.row_values(i) for i in range(1, stock_rows)]
store_stock.sort(key = lambda x: x[ID_index])

#合并相同ID的货品,将数量和金额进行相加
def getOutput(store, rows):
	out = []
	for i in range(1, rows-1):
		if store[i][ID_index] == store[i-1][ID_index]:
			store[i][amount_index] += store[i-1][amount_index]
			store[i][money_index] += store[i-1][money_index]
		else:
			out.append(store[i-1])
	out.append(store[rows-2])
	return out

out_sold = getOutput(store_sold, sold_rows)
out_stock = getOutput(store_stock, stock_rows)

#合并以后如果两个表的行数不一致，应该是原始数据有问题，没有处理异常。。
#if len(out_sold) != len(out_stock):
#	print("行数不相等")

#把合并操作完成后的两张表写到Excel文件，这个可用于调试检查，不需要中间结果的话可以注释
file_out = xlsxwriter.Workbook(u'中间结果.xlsx')
sold = file_out.add_worksheet(u'销售处理后的结果')
stock = file_out.add_worksheet(u'进货处理后的结果')
for i in range(sold_cols):
	sold.write(0, i, colname[i])    #写第一行
for i in range(len(out_sold)):
	for j in range(sold_cols):
		sold.write(i+1, j, out_sold[i][j])   #写内容

for i in range(stock_cols):
	stock.write(0, i, colname[i])
for i in range(len(out_stock)):
	for j in range(stock_cols):
		stock.write(i+1, j, out_stock[i][j])

#计算上面两张表的差异，将最终结果写到新的Excel文件中
result = xlsxwriter.Workbook(u'最终结果.xlsx')
out = result.add_worksheet(u'差异结果')
for i in range(sold_cols):
	out.write(0, i, colname[i])

index = 1
tmp = 0
for i in range(len(out_sold)):
	tmp = -1
	for j in range(len(out_stock)):
		if out_sold[i][ID_index] == out_stock[j][ID_index]:
			tmp = j
			break
	if tmp == -1:
		for k in range(sold_cols):
			out.write(index, k, out_sold[i][k])
		index += 1
	else:
		if not(out_sold[i][amount_index] == out_stock[tmp][amount_index] and out_sold[i][money_index] == out_stock[tmp][money_index]):
			for k in range(sold_cols):
				if k == amount_index or k == money_index:
					out.write(index, k, out_sold[i][k] - out_stock[tmp][k])
				else:
					out.write(index, k, out_sold[i][k])
			index += 1

file_out.close()
result.close()



