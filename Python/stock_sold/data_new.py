# -*- coding: utf-8 -*-
# Author: Chao Gao
# manipulating data

import xlrd
import datetime
import xlsxwriter

data = xlrd.open_workbook(u"test_new.xlsx")

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

#这几个列属性是有用的
ID_index = colname.index(u'货品ID')
amount_index = colname.index(u'数量')
money_index = colname.index(u'金额')
fapiao_index = colname.index(u'发票号')
time_index = colname.index(u'发票日期')

#除去第一行都是有效数据，每一行作为一个元素存储到列表中，并进行排序
#excel里面的日期是用float类型存的，还要做一下转化，这里转换写的很丑。。。
store_sold = [table_sold.row_values(i) for i in range(1, sold_rows)]
for i in range(sold_rows-1):
	if store_sold[i][time_index] != "":
		store_sold[i][time_index] = (xlrd.xldate_as_tuple(store_sold[i][time_index], 0))
		store_sold[i][time_index] = str(store_sold[i][time_index][0]) + "/" + str(store_sold[i][time_index][1]) + "/" + str(store_sold[i][time_index][2])
store_sold.sort(key = lambda x: x[fapiao_index])
store_stock = [table_stock.row_values(i) for i in range(1, stock_rows)]
for i in range(stock_rows-1):
	if store_stock[i][time_index] != "":
		store_stock[i][time_index] = (xlrd.xldate.xldate_as_tuple(store_stock[i][time_index], 0))
		store_stock[i][time_index] = str(store_stock[i][time_index][0]) + "/" + str(store_stock[i][time_index][1]) + "/" + str(store_stock[i][time_index][2])
store_stock.sort(key = lambda x: x[fapiao_index])

#每一个发票号就是一个块
def getBlock(store, rows):
	block = []
	first = 0
	for i in range(1, rows-1):
		if store[i][fapiao_index] != store[i-1][fapiao_index]:
			temp = [store[x] for x in range(first, i)]
			block.append(temp)
			first = i
	temp = [store[x] for x in range(first, rows-1)]
	block.append(temp)
	return block

block_sold = getBlock(store_sold, sold_rows)
block_stock = getBlock(store_stock, stock_rows)

#每个发票号的块内部使用ID排序
for i in range(0, len(block_sold)):
	block_sold[i].sort(key = lambda x: x[ID_index])
for i in range(0, len(block_stock)):
	block_stock[i].sort(key = lambda x: x[ID_index])

#合并相同ID的货品,将数量和金额进行相加
def getOutput(store, rows):
	out = []
	for i in range(1, rows):
		if store[i][ID_index] == store[i-1][ID_index]:
			store[i][amount_index] += store[i-1][amount_index]
			store[i][money_index] += store[i-1][money_index]
		else:
			out.append(store[i-1])
	out.append(store[rows-1])
	return out

out_sold = [getOutput(block_sold[i], len(block_sold[i])) for i in range(0, len(block_sold))]
out_stock = [getOutput(block_stock[i], len(block_stock[i])) for i in range(0, len(block_stock))]

#把合并操作完成后的两张表写到Excel文件，这个可用于调试检查，不需要中间结果的话可以注释
file_out = xlsxwriter.Workbook(u'中间结果.xlsx')
sold = file_out.add_worksheet(u'销售处理后的结果')
stock = file_out.add_worksheet(u'进货处理后的结果')

def writeMiddleResult(out_f, in_f, cols):
	for i in range(cols):
		out_f.write(0, i, colname[i])    #写第一行

	index = 0
	for i in range(len(in_f)):
		for j in range(len(in_f[i])):
			for k in range(cols):				
				out_f.write(index+1, k, in_f[i][j][k])   #写内容
			index += 1
writeMiddleResult(sold, out_sold, sold_cols)
writeMiddleResult(stock, out_stock, stock_cols)

#计算上面两张表的差异，将最终结果写到新的Excel文件中
result = xlsxwriter.Workbook(u'最终结果.xlsx')
out = result.add_worksheet(u'差异结果')
for i in range(sold_cols):
	out.write(0, i, colname[i])


#找到与销售单发票号相等的进货块
def getBlockIndex(sold, out_stock):
	for i in range(len(out_stock)):
		if out_stock[i][0][fapiao_index] == sold[0][fapiao_index]:
			return i
	return -1


index = 1
tmp = 0
for m in range(len(out_sold)):
	block_index = getBlockIndex(out_sold[m], out_stock)
	#进货没有对应销售发票号的块，直接写销售的条目
	if block_index == -1:
		for i in range(len(out_sold[m])):
			for j in range(sold_cols):
				out.write(index, j, out_sold[m][i][j])
			index += 1
	else:
		for i in range(len(out_sold[m])):
			tmp = -1
			for j in range(len(out_stock[block_index])):
				if out_sold[m][i][ID_index] == out_stock[block_index][j][ID_index]:
					tmp = j
					break
			if tmp == -1:
				for k in range(sold_cols):
					out.write(index, k, out_sold[m][i][k])
				index += 1
			else:
				if not(out_sold[m][i][amount_index] == out_stock[block_index][tmp][amount_index] and out_sold[m][i][money_index] == out_stock[block_index][tmp][money_index]):
					for k in range(sold_cols):
						if k == amount_index or k == money_index:
							out.write(index, k, out_sold[m][i][k] - out_stock[block_index][tmp][k])
						else:
							out.write(index, k, out_sold[m][i][k])
					index += 1

file_out.close()
result.close()




