#!/usr/src/env python
# -*- coding: utf-8 -*-
#author: Chao Gao

#exploratory data analysis to determine if the gap between .. has increased
#the income inequality

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# For this assignment, we need to load in the following modules
import requests
import StringIO
import zipfile
import scipy.stats 

url = "https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv"
s = StringIO.StringIO(requests.get(url).content)
countries = pd.read_csv(s)
print countries.head()

#due to the Wall I download it to the local area
#income_link = 'https://spreadsheets.google.com/pub?key=phAwcNAVuyj1jiMAkmq1iMg&output=xls'
#source = StringIO.StringIO(requests.get(income_link).content)
income = pd.read_excel('data.xlsx', sheetname = "Data")
print income.head()

income.index = income[income.columns[0]]
income = income.drop(income.columns[0], axis = 1)
income.columns = map(lambda x: int(x), income.columns)
income = income.transpose()
print income.head()
#print income.columns[0]

year = 2000
plt.plot(subplots=True)
plt.hist(income.ix[year].dropna().values, bins = 20)
plt.title('Year: %i' % year)
plt.xlabel('Income per person')
plt.ylabel('Frequency')
plt.show()

plt.hist(np.log10(income.ix[year].dropna().values), bins = 20)
plt.title('Year: %i' % year)
plt.xlabel('Income per person (log10 scale)')
plt.ylabel('Frequency')
plt.show()

def mergeByYear(year):
    data = pd.DataFrame(income.ix[year].values, columns = ['Income'])
    data['Country'] = income.columns
    joined = pd.merge(data, countries, how = 'inner', on = ['Country'])
    joined.Income = np.round(joined.Income, 2)
    return joined
print mergeByYear(2010).head()

years = np.arange(1950, 2010, 10)
for yr in years:
    df = mergeByYear(yr)
    df.boxplot('Income', by = 'Region', rot = 90)
    plt.title('Year:' + str(yr))
    plt.ylabel('Income per person(log10 scale)')
    plt.ylim(10 ** 2, 10.5 ** 5)
    plt.yscale('log')
    plt.show()

