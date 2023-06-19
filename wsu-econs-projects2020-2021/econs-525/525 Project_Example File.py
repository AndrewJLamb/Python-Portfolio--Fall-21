#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 14:05:16 2021

@author: andrew7
"""

import pandas as pd
import numpy as np
import patsy as pt
import matplotlib.pyplot as plt
import statsmodels.api as sm 
import statsmodels.stats.outliers_influence as smo
import statsmodels.formula.api as smf

#EconS525 Research Project
#Importing dataset
df = pd.read_excel("/Users/andrew7/Desktop/[EconS525]/525 PROJECT/FINALDATASET.xlsx")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#print(f'df.head(): \n{df.head()}\n')                                   
#print(f'df.tail(): \n{df.tail()}\n') 

#printing T;
T = len(df)
print(f'T: \n{T}\n')

#Checking shape of our dataset
print(f'df.shape: {df.shape}\n')

#Deriving Import Price Level;
df['hts50imp_p'] = df['hts50impVal']/df['hts50impQuan']
df['hts51imp_p'] = df['hts51impVal']/df['hts51impQuan']
df['hts52imp_p'] = df['hts52impVal']/df['hts52impQuan']
df['hts53imp_p'] = df['hts53impVal']/df['hts53impQuan']
df['hts54imp_p'] = df['hts54impVal']/df['hts54impQuan']
df['hts55imp_p'] = df['hts55impVal']/df['hts55impQuan']
df['hts56imp_p'] = df['hts56impVal']/df['hts56impQuan']
df['hts58imp_p'] = df['hts58impVal']/df['hts58impQuan']
df['hts60imp_p'] = df['hts60impVal']/df['hts60impQuan']
df['hts61imp_p'] = df['hts61impVal']/df['hts61impQuan']
df['hts62imp_p'] = df['hts62impVal']/df['hts62impQuan']

#Deriving Export Price level;
df['hts50exp_p'] = df['hts50expVal']/df['hts50expQuan']
df['hts51exp_p'] = df['hts51expVal']/df['hts51expQuan']
df['hts52exp_p'] = df['hts52expVal']/df['hts52expQuan']
df['hts53exp_p'] = df['hts53expVal']/df['hts53expQuan']
df['hts54exp_p'] = df['hts54expVal']/df['hts54expQuan']
df['hts55exp_p'] = df['hts55expVal']/df['hts55expQuan']
df['hts56exp_p'] = df['hts56expVal']/df['hts56expQuan']
df['hts58exp_p'] = df['hts58expVal']/df['hts58expQuan']
df['hts60exp_p'] = df['hts60expVal']/df['hts60expQuan']
df['hts61exp_p'] = df['hts61expVal']/df['hts61expQuan']
df['hts62exp_p'] = df['hts62expVal']/df['hts62expQuan']


#Creating dummy variable for 'trade war':
# '0318_0918' = Obs. in Mar. 2018 thru Sept. 2018;
# Noted on timeline to be a tumultuous period for 
#U.S.-China trade negotiations, retaliation;
df['d_tradewar0318_0918'] = ((df['Date'] >='2018-02-01') 
                             & (df['Date'] <='2018-10-01')).astype(int)

#Creating dummy variable for 'trade war':
# '0419_0919' = Obs. in Apr. 2019 thru Sept. 2019;
# Noted on timeline to be a tumultuous period for 
#U.S.-China trade negotiations, retaliation;
df['d_tradewar0419_0919'] = ((df['Date'] >='2019-03-01') 
                             & (df['Date'] <='2019-10-01')).astype(int)

#Creating interaction term between:
#hts(xx) import prices
# and dummy variable 'trade war'
# '0318_0918' = Obs. in Mar. 2018 thru Sept. 2018;
df['d_hts52imp_p_x_tradewar0318_0918'] = df.hts52imp_p*df.d_tradewar0318_0918

#Creating interaction term between:
#hts(xx) import prices
# and dummy variable 'trade war'
#'0418_0919' = Obs. in Apr. 2019 thru Sept. 2019 ;

df['d_hts52imp_p_x_tradewar0419_0919'] = df.hts52imp_p*df.d_tradewar0419_0919


#Creating interaction term between hts(xx) import prices
# and their corrsponding Ad Valorem duty rates;
df['hts50imp_p_x_hts50AdVal'] = df.hts50impQuan*df.hts50AdVal 
df['hts51imp_p_x_hts51AdVal'] = df.hts51impQuan*df.hts51AdVal 
df['hts52imp_p_x_hts52AdVal'] = df.hts52impQuan*df.hts52AdVal 
df['hts53imp_p_x_hts53AdVal'] = df.hts53impQuan*df.hts53AdVal 
df['hts54imp_p_x_hts54AdVal'] = df.hts54impQuan*df.hts54AdVal 
df['hts55imp_p_x_hts55AdVal'] = df.hts55impQuan*df.hts55AdVal 
df['hts56imp_p_x_hts56AdVal'] = df.hts56impQuan*df.hts56AdVal 
df['hts58imp_p_x_hts58AdVal'] = df.hts58impQuan*df.hts58AdVal 
df['hts60imp_p_x_hts60AdVal'] = df.hts60impQuan*df.hts60AdVal 
df['hts61imp_p_x_hts61AdVal'] = df.hts61impQuan*df.hts61AdVal 
df['hts62imp_p_x_hts62AdVal'] = df.hts62impQuan*df.hts62AdVal 

#Summarizing all data;
Data_summary = df.describe()
#print(f'Data_summary:\n{Data_summary}\n')

#Finding the correlation coeficients for all data;
Corr_coef = df.corr()
#print(f'Corr_coef:\n{Corr_coef}\n')


### time series plots of derived import prices: ###
#plt.plot('hts50imp_p', data=df, color='black', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts51imp_p', data=df, color='black', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts52imp_p', data=df, color='black', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts53imp_p', data=df, color='black', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts54imp_p', data=df, color='black', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts55imp_p', data=df, color='black', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts56imp_p', data=df, color='black', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts58imp_p', data=df, color='black', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts60imp_p', data=df, color='black', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts61imp_p', data=df, color='black', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts62imp_p', data=df, color='black', linestyle='-')
#plt.show()
#plt.close()

### time series plots of derived export prices: ###
#plt.plot('hts50exp_p', data=df, color='blue', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts51exp_p', data=df, color='blue', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts52exp_p', data=df, color='blue', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts53exp_p', data=df, color='blue', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts54exp_p', data=df, color='blue', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts55exp_p', data=df, color='blue', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts56exp_p', data=df, color='blue', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts58exp_p', data=df, color='blue', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts60exp_p', data=df, color='blue', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts61iexp_p', data=df, color='blue', linestyle='-')
#plt.show()
#plt.close()
#plt.plot('hts62exp_p', data=df, color='blue', linestyle='-')
#plt.show()
#plt.close()

#Replacing 'inf' values with NaN's;
df.replace([np.inf, -np.inf], np.nan,inplace=True)
#dropping 'inf' values that were converted to NaN;
df = df.dropna()
#Checking the head and tail of the data;
#print(f'df.head(): \n{df.head()}\n')                                   
#print(f'df.tail(): \n{df.tail()}\n') 


#DiD_noC: Without control var.'s; 
#Containing DiD (no control var.'s) regression components within a DataFrame;
y1, X1Mat = pt.dmatrices(
    'USACPI_03 ~ 1 + d_tradewar0318_0918 + d_tradewar0419_0919'
    ' + hts50imp_p + hts51imp_p + hts52imp_p + hts53imp_p'
    ' + hts54imp_p + hts55imp_p + hts56imp_p + hts58imp_p'
    ' + hts60imp_p + hts61imp_p + hts62imp_p + hts50exp_p'
    ' + hts51exp_p + hts52exp_p + hts53exp_p + hts54exp_p'
    ' + hts55exp_p + hts55exp_p + hts56exp_p + hts58exp_p'
    ' + hts60exp_p + hts61exp_p + hts62exp_p'
    ' + d_hts52imp_p_x_tradewar0318_0918 + d_hts52imp_p_x_tradewar0419_0919'
                   ,data=df, return_type='dataframe') 



# Difference-in-Difference without control variables;
reg5_did = smf.ols(formula=
                   'USACPI_03 ~ 1 + d_tradewar0318_0918 + d_tradewar0419_0919'
                   ' + hts50imp_p + hts51imp_p + hts52imp_p + hts53imp_p'
                   ' + hts54imp_p + hts55imp_p + hts56imp_p + hts58imp_p'
                   ' + hts60imp_p + hts61imp_p + hts62imp_p + hts50exp_p'
                   ' + hts51exp_p + hts52exp_p + hts53exp_p + hts54exp_p'
                   ' + hts55exp_p + hts55exp_p + hts56exp_p + hts58exp_p'
                   ' + hts60exp_p + hts61exp_p + hts62exp_p'
                   ' + d_hts52imp_p_x_tradewar0318_0918 + d_hts52imp_p_x_tradewar0419_0919'
                   ,data=df)
results5_did = reg5_did.fit()
#print regression table:
table5_did = pd.DataFrame({'b': round(results5_did.params, 4),
                          'se': round(results5_did.bse, 4),
                          't': round(results5_did.tvalues, 4),
                          'pval': round(results5_did.pvalues, 4)})
print(f'results5_did.summary(): \n{results5_did.summary()}\n')
print(f'table5_did: \n{table5_did}\n')

#Testing model VIF's (DiD_noC) without control variables;
#VIF's for DiD;
K1 = X1Mat.shape[1]
VIF_noC = np.empty(K1)
for i in range(K1):
    VIF_noC[i] = smo.variance_inflation_factor(X1Mat.values, i)
print(f'VIF(Model_noC): \n{VIF_noC}\n')  

#DiD_C: Adding control var.'s;
#Containing DiD_C (w/ control var.'s) regression components within a DataFrame;
y2C, X2MatC = pt.dmatrices(
    'USACPI_03 ~ 1 + CHNCPI + USACPI + np.log(USAPersonalIncome)'
    ' + C(Month) + C(Year)'
    ' + d_tradewar0318_0918 + d_tradewar0419_0919'
    ' + hts50imp_p + hts51imp_p + hts52imp_p + hts53imp_p'
    ' + hts54imp_p + hts55imp_p + hts56imp_p + hts58imp_p'
    ' + hts60imp_p + hts61imp_p + hts62imp_p + hts50exp_p'
    ' + hts51exp_p + hts52exp_p + hts53exp_p + hts54exp_p'
    ' + hts55exp_p + hts55exp_p + hts56exp_p + hts58exp_p'
    ' + hts60exp_p + hts61exp_p + hts62exp_p'
    ' + d_hts52imp_p_x_tradewar0318_0918 + d_hts52imp_p_x_tradewar0419_0919'
                   ,data=df, return_type='dataframe') 


#Difference-in-difference (DiD_C) with control variables;
reg5_didC = smf.ols(formula=
                   'USACPI_03 ~ 1 + CHNCPI + USACPI + np.log(USAPersonalIncome) '
                   '+ C(Month) + C(Year)'
                   ' + d_tradewar0318_0918 + d_tradewar0419_0919'
                   ' + hts50imp_p + hts51imp_p + hts52imp_p + hts53imp_p'
                   ' + hts54imp_p + hts55imp_p + hts56imp_p + hts58imp_p'
                   ' + hts60imp_p + hts61imp_p + hts62imp_p + hts50exp_p'
                   ' + hts51exp_p + hts52exp_p + hts53exp_p + hts54exp_p'
                   ' + hts55exp_p + hts55exp_p + hts56exp_p + hts58exp_p'
                   ' + hts60exp_p + hts61exp_p + hts62exp_p'
                   ' + d_hts52imp_p_x_tradewar0318_0918 + d_hts52imp_p_x_tradewar0419_0919'
                   ,data=df)
results5_didC = reg5_didC.fit()
#print regression table:
table5_didC = pd.DataFrame({'b': round(results5_didC.params, 4),
                          'se': round(results5_didC.bse, 4),
                          't': round(results5_didC.tvalues, 4),
                          'pval': round(results5_didC.pvalues, 4)})

print(f'results5_didC.summary(): \n{results5_didC.summary()}\n')
print(f'table5_didC: \n{table5_didC}\n')

#Testing model VIF's- (DiDC) with control variables;
#VIF's for DiD;
K2 = X2MatC.shape[1]
VIF_C = np.empty(K2)
for i in range(K2):
    VIF_C[i] = smo.variance_inflation_factor(X2MatC.values, i)
print(f'VIF(Model_C): \n{VIF_C}\n')    







