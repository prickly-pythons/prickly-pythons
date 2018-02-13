# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 14:05:14 2018

@author: chinm
"""

# Prickly Pythons

# 0b - binary, 0x - hexadecimal , base pi, base i
#pi,i -Non integer representation
#pd.merge - merge spreadsheets
#
import pandas as pd
import matplotlib.pyplot as plt

df_load = pd.read_excel('Loaddata.xlsx',skiprows=0)
#print(df_load.head())
#df_date= pd.to_datetime(df_load['Usage Date'])
df_load['Usage Date'] = pd.to_datetime(df_load['Usage Date'])
df_load.index = df_load['Usage Date']
del df_load['Usage Date']
df_load.groupby(['Usage Date']).count()
#df_load.resample('D').mean()
#df_load.resample('D').sum()
df_load.resample('W').sum().plot()
#fig, ax1 = plt.subplots()
#
#ax2 = ax1.twinx()
#ax1.plot(df_load.index, df_load['Cost'], 'g-')
#ax2.plot(df_load.index, df_load['kWh'], 'b-')
#
#ax1.set_xlabel('Date')
#ax1.set_ylabel('Cost', color='g')
#ax2.set_ylabel('kWh', color='b')
#
plt.show()
#plt.rcParams['figure.figsize'] = 12,5
