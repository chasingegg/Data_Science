#!/usr/src/env python
# -*- coding: utf-8 -*-
#author: Chao Gao

#if group A has larger values than group B on average, does it mean the largest values are from group A
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests
import StringIO
import zipfile
import scipy.stats

url = "https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv"
s = StringIO.StringIO(requests.get(url).content)
countries = pd.read_csv(s)

#due to the Wall I download it to the local area
#income_link = 'https://spreadsheets.google.com/pub?key=phAwcNAVuyj1jiMAkmq1iMg&output=xls'
#source = StringIO.StringIO(requests.get(income_link).content)
income = pd.read_excel('data.xlsx', sheetname = "Data")

income.index = income[income.columns[0]]
income = income.drop(income.columns[0], axis = 1)
income.columns = map(lambda x: int(x), income.columns)
income = income.transpose()
#the proportion of X > a compare to the proportion of Y > a
def ratioNormals(diff, a):
    X = scipy.stats.norm(loc = diff, scale = 1)
    Y = scipy.stats.norm(loc = 0, scale = 1)
    return X.sf(a) / Y.sf(a)

diffs = np.linspace(0, 5, 50)
a_values = range(2, 6)

plt.figure(figsize = (8, 5))
for a in a_values:
    ratios = [ratioNormals(diff, a) for diff in diffs]
    plt.plot(diffs, ratios)


plt.legend(["a={}".format(a) for a in a_values], loc = 0)
plt.xlabel('Diff')
plt.ylabel('Pr(X > a) / Pr(Y > a)')
plt.title('Ratio of Pr(X > a) to Pr(Y > a) as a Function of Diff')
plt.yscale('log')
plt.show()

# now consider the distribution of income per person from two regions
def mergeByYear(year):
    data = pd.DataFrame(income.ix[year].values, columns = ['Income'])
    data['Country'] = income.columns
    joined = pd.merge(data, countries, how = 'inner', on = ['Country'])
    joined.Income = np.round(joined.Income, 2)
    return joined

merged = mergeByYear(2012).groupby('Region', as_index = False).mean()
merged = merged.loc[(merged.Region == 'ASIA') | (merged.Region == 'SOUTH AMERICA')]
merged.Income = np.round(merged.Income, 2)
print merged

df = mergeByYear(2012)
df = df.loc[(df.Region == "ASIA") | (df.Region == "SOUTH AMERICA")]
df.boxplot('Income', by = 'Region', rot = 90)
plt.ylabel('Income per person (dollars)')
plt.show()

df = mergeByYear(2012)
df = df.loc[(df.Region == "ASIA") | (df.Region == "SOUTH AMERICA")]
df.boxplot('Income', by = 'Region', rot = 90)
plt.ylabel('Income per person (log10 scale)')
plt.yscale('log')
plt.show()

def ratioCountries(groupedData, a):
    prop = [len(group.Income[group.Income >= a]) / float(len(group.Income.dropna())) for key, group in groupedData]
    z = pd.DataFrame(groupedData.mean().index, columns = ['Region'])
    z['Mean'] = np.round(groupedData.mean().values,2)
    z['P(X > %g)' % a] = np.round(prop, 4)
    return z

df = mergeByYear(2012).groupby('Region')
df_ratio = ratioCountries(df, 1e4)
df_ratio = df_ratio[(df_ratio.Region == 'ASIA') | (df_ratio.Region == 'SOUTH AMERICA')]
print df_ratio

population_link = 'https://spreadsheets.google.com/pub?key=phAwcNAVuyj0XOoBL_n5tAQ&output=xls'
source = StringIO.StringIO(requests.get(population_link).content)
population = pd.read_excel(source, sheetname = "Data")

# Put years as index and countries as column names
population.columns = ['Country'] + map(int, list(population.columns)[1:])
print population.head()

def mergeByYearWithPop(year):

    # income DataFrame
    income_df = pd.DataFrame(income.ix[year].values, columns = ['Income'])
    income_df['Country'] = income.columns

    # merge income DataFrame and countries
    joined = pd.merge(income_df, countries, how="inner", on=['Country'])
    
    # population DataFrame
    population_df = population[['Country',year]]

    # merge population DataFrame and joined DataFrame 
    joined = pd.merge(joined, population_df, how="inner", on=['Country'])
    joined.columns = list(joined.columns[:-1])+['TotalPopulation']
    joined.Income = np.round(joined.Income, 2)
    
    def func(df):
        totPop = df.sum()['TotalPopulation']
        dfout = df
        dfout['AdjustedIncome'] = df.Income * df.TotalPopulation / float(totPop)
        dfout.AdjustedIncome = np.round(dfout.AdjustedIncome, 2)
        return dfout
        
    # Group by region
    returnDataFrame = joined.groupby('Region').apply(func)
    return returnDataFrame

print mergeByYearWithPop(2012).head()

df = mergeByYearWithPop(2012).groupby('Region').sum()
df.Income = mergeByYear(2012).groupby('Region').mean().Income
df.Income = np.round(df.Income, 2)
df = df.ix[['ASIA', 'SOUTH AMERICA']]
print df

df = mergeByYearWithPop(2012)
df.AdjustedIncome = df['AdjustedIncome']
df = df[(df.Region == 'ASIA') | (df.Region == 'SOUTH AMERICA')]
df.boxplot('AdjustedIncome', by = 'Region', rot = 90)
plt.yscale('log')
plt.ylabel('Income per person adjusted for population (log10 scale)')
plt.show()

def ratioCountries(groupedData, a):
    prop = [len(group.AdjustedIncome[group.AdjustedIncome >= a]) / float(len(group.AdjustedIncome.dropna())) for key, group in groupedData]
    z = pd.DataFrame(groupedData.mean().index, columns = ['Region'])
    z['AdjustedIncome'] = np.round(groupedData.AdjustedIncome.sum().values,2)
    z['P(X > %g)' % a] = np.round(prop,4)
    return z

df = mergeByYearWithPop(2012).groupby('Region')
df_ratio = ratioCountries(df, 1e4)
df_ratio = df_ratio[(df_ratio.Region == 'ASIA') | (df_ratio.Region == 'SOUTH AMERICA')]
print df_ratio

df = mergeByYearWithPop(2012).groupby('Region')
df_ratio = ratioCountries(df, 1e3)
df_ratio = df_ratio[(df_ratio.Region == 'ASIA') | (df_ratio.Region == 'SOUTH AMERICA')]
print df_ratio