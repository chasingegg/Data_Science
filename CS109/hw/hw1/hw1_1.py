#!/Users/dimon//anaconda2/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests
import StringIO
import zipfile
import scipy.stats

#extract all the text files from the web
#the zipfile model can create, read, write, append and list ZIP files
def getZIP(zipFileName):
	r = requests.get(zipFileName).content
	s = StringIO.StringIO(r)
	zf = zipfile.ZipFile(s, 'r')
	return zf

url = 'http://seanlahman.com/files/database/lahman-csv_2014-02-14.zip'
zf = getZIP(url)
print zf.namelist()

#extract the 'Salaries.csv' file from the zipped folder
#zf.open()function to open a file
#pd.read_csv() to read the table into a pandas DataFrame
tablenames = zf.namelist()
print tablenames[tablenames.index('Salaries.csv')]

salaries = pd.read_csv(zf.open(tablenames[tablenames.index('Salaries.csv')]))
#print salaries
print "Number of rows: %i" % salaries.shape[0] #输出维度
print salaries.head() #输出前五行

#extract the 'Teams.csv' file from the zipped folder
teams = pd.read_csv(zf.open(tablenames[tablenames.index('Teams.csv')]))
teams = teams[['yearID', 'teamID', 'W']]
print 'Number of rows: %i' % teams.shape[0]
print teams.head()

#summarize the Salaries DataFrame to show the total salaries for each team for each year
totSalaries = salaries.groupby(['yearID', 'teamID'], as_index = False).sum()
print totSalaries.head()

#merge two DataFrames
joined = pd.merge(totSalaries, teams, how = 'inner', on = ['yearID', 'teamID'])
print joined.head()

#create a scatter plot to graphically display the relatioship between total wins and total salaries
#we will consider the Oakland baseball team 
teamName = 'OAK'
years = np.arange(2000, 2004)
for yr in years:
	df = joined[joined['yearID'] == yr]
	plt.scatter(df['salary'] / 1e6, df['W'])
	plt.title('Wins versus Salaries in year ' + str(yr))
	plt.xlabel('Total Salary (in millions)')
	plt.ylabel('Wins')
	plt.xlim(0, 180)
	plt.ylim(30, 130)
	plt.grid()
	plt.annotate(teamName, 
        xy = (df['salary'][df['teamID'] == teamName] / 1e6,  df['W'][df['teamID'] == teamName]), 
        xytext = (-20, 20), textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', facecolor = 'black' , connectionstyle = 'arc3,rad=0'))
	plt.show()

#calculate the least squares estimate of the coefficients in a linear regression model
#calculate the residuals for each team
teamName = 'OAK'
years = np.arange(1999, 2005)
residData = pd.DataFrame()

for yr in years:
	df = joined[joined['yearID'] == yr]
	x_list = df['salary'].values / 1e6
	y_list = df['W'].values

	#least squares estimates
	A = np.array([x_list, np.ones(len(x_list))])
	y = y_list
	w = np.linalg.lstsq(A.T, y)[0] #coefficient
	yhat = (w[0] * x_list + w[1]) #regression line
	residData[yr] = y - yhat

residData.index = df['teamID']
residData = residData.T
residData.index = residData.index.format()
residData.plot(title = 'Residuals from least squares estimates across years', figsize =(15,8),color=map(lambda x:'blue' if x=='OAK' else 'gray', df.teamID))

plt.xlabel('Year')
plt.ylabel('Residuals')
plt.show()








