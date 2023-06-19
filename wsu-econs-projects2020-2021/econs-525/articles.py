#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 13:07:35 2021

@author: andrew7
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:04:37 2021

@author: andrew7
"""

import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt

# Display and Plotting
import matplotlib.pylab as plt
import seaborn as sns
import datetime as dt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.dates as mdates

#Operations
import patsy as pt
import numpy as np 
import pandas as pd 
import linearmodels as plm


###                      ANDREW LAMB (ID: 011442507)                       ###
###                      WASHINGTON STATE UNIVERSITY                       ###
###                      EconS 702 Research Project                        ###

#   Importing 'arti.csv':
#Call brings in the following recorded observations for: 
#   Export quantities, values, derived price levels GDP, CPI, 
#   population, and exchange rates for the following countries:
#    United States, India, China, Japan, and Korea;
#For dates ranging:    
    #May 2009 thru (latest) June 2021;
#DATA: 

    # 'id' = Unique values assigned to Country Entities;
    #      = 1 = United States; 
    #      = 2 = China; 
    #      = 3 = India; 
    #      = 4 = Japan;
    #      = 5 = Korea; 

# 'year' = Corresponding year that data was observed for;
    # Ranges from 2009 through the first 1-2 months of 2021

# 'month' = Corresponding month that data was observed for;
    # Ranges from May 2009 through Feb. 2021
    #     = 1 = Jan.; = 2 = Feb., and so forth.

# 'dest' = Unique values assigned to the Destination Country; 
    #      = 1 = United States; 
    #      = 2 = China; 
    #      = 3 = India; 
    #      = 4 = Japan;
    #      = 5 = Korea; 

# 'hts' = Unique values assigned the observation belonging to various
#         Harmonized Tariff Schedule (HTS) categories:
# Source: United States Int'l Trade Comission, 
# Harmonized Tariff Schedule of the United States (2021) Basic Revision 7
    #      = 1 = HS50: Silk
    #      = 2 = HS51: Wool, fine or coarse animal hair;
    #               horsehair yarn and woven fabric
    #      = 3 = HS52: Cotton
    #      = 4 = HS53: Other vegetable textile fibers; paper yarn 
    #               and woven fabric of paper yarn
    #      = 5 = HS54: Man-made filaments 
    #      = 6 = HS55: Man-made staple fibers 
    #      = 7 = HS56: Wadding, felt and nonwovens; special yarns, 
    #               twine, cordage, ropes and cables and articles thereof 
    #      = 8 = HS58: Special woven fabrics; tufted textile fabrics;
    #               lace, tapestries; trimmings; embroidery 
    #      = 9 = HS60: Knitted or crocheted fabrics
    #     = 10 = HS61: Articles of apparel and clothing accessories,
    #               knitted or crocheted
    #     = 11 = HS62: Articles of apparel and clothing accessories,
    #               not knitted or crocheted
    #     = 12 = HS63: Other made up textile articles; sets; worn 
    #               clothing and worn textile articles; rags

# 'q' = Exported Quantity (in either kilograms or sq. meters);
    #Source: International Trade Centre- TradeMap: 
        # See: 'List of Importing Markets for {Country}'
        #HS 2-Digit Categories Used: 
            # (HS) 50, 51, 52, 53, 54, 55... 
            #   ...56, 58, 60, 61, 62, 63
        # URL:  https://www.intracen.org/itc/market-info-tools/trade-statistics/
        # trademap.org

# 'v' = Exported Value (in US$1,000);
    #Source: International Trade Centre- TradeMap:
         #HS 2-Digit Categories Used: 
            # (HS) 50, 51, 52, 53, 54, 55... 
            #   ...56, 58, 60, 61, 62, 63
        # See: 'List of Importing Markets for {Country}'
        # URL:  https://www.intracen.org/itc/market-info-tools/trade-statistics/
        # trademap.org

# 'cpi' = Consumer Price Index- Total, All Items for {Country};
    #Source: Federal Reserve Economic Data
    # URL: fred.stlouisfed.org

# 'gdp' = Leading Indicators OECD: Reference series:
#         Gross Domestic Product (GDP): Normalised for {Country},
#         Index, Monthly, Seasonally Adjusted

# 'pop' = {Country} Population, yearly 
    #Source: https://data.worldbank.org/indicator/SP.POP.TOTL

# 'exch' = Monthly Exchange rate, Not Seasonally Adjusted;
    #Source: Federal Reserve Economic Data
    # URL: fred.stlouisfed.org

# 'date' = Date assigned to index, in format (YYYY)-(MM)

# 'p' = Derived Export Price level; 
    # (See: Line 130) Eq. = Export Quan. / Export Val.;
    #Source for Export Quan., Val data:
        # International Trade Centre- TradeMap
        # trademap.org


#Specifying pandas printing options;
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
#Import csv data file. Return type from function is a pandas DataFrame
#'at' is short for (A)pp(T)ex, the pet name I've given this project
    # (A)pp(T)ex = "(A)pparel and (T)extiles "
ar = pd.read_csv('/Users/andrew7/'
                 'Desktop/[EconS702]/'
                 'DATA/'
                 'STACK/'
                 'panels_consolidated/'
                 'panel_stack/ready/'
                 'groups_files/'
                 'arti.csv',
                 index_col = ['Country', 'date'],
                 parse_dates =[2])
#https://bashtage.github.io/linearmodels/devel/panel/examples/data-formats.html
ar['date'] = pd.to_datetime(ar[['year', 'month']].assign(DAY=1))

# Replacing inf's with Nan's; and Filling NaN's with zeros; 
ar.replace([np.inf, -np.inf], np.nan, inplace=True)
ar = ar.fillna(0)


# PRICE LEVELS:
#Deriving price levels;
#Threads group
q = ar['q']
v = ar['v']
#Quan., Val. of type float
ar.v.astype(float)
ar.q.astype(float)
#Dividing value of threads exports by their corresponding quantities;
ar['p'] = v / q
# Replacing inf's with Nan's; and Filling NaN's with zeros;
#   Note: Price eq. often times resulted in inf or NaN values
ar.replace([np.inf, -np.inf], np.nan, inplace=True)
ar = ar.fillna(0)


#DUMMY VARIABLES:
#Creating dummy variables for the following:
    # Country (= __ if [id] == __);
    # Trade War ( = __ if [date] in __); 
    # COVID     ( = __ if [date] in __); 
    # Destination (= __ if [id] == __);
#Country
#Creating dummy variable for 'Country':
dCountry = pd.get_dummies(ar.id, prefix='d_id')
ar = pd.concat([ar,dCountry], axis=1)

#Destination
#Creating dummy variable for 'dest':
ddest = pd.get_dummies(ar.dest, prefix='ddest')
ar = pd.concat([ar,ddest], axis=1)


#HS Category
#Creating dummy variable for 'hscode':
dhts = pd.get_dummies(ar.hscode, prefix='dhts')
ar = pd.concat([ar, dhts], axis=1)


#Trade War
#Creating dummy variable for 'trade war':
# 'tw1' = Obs. in Apr. 2018 thru May 2018;
#Noted on timeline to be a time period of interest for 
    #U.S.-China trade negotiations, retaliation;
ar['tw1'] = ((ar['date'] >='2018-03') 
                             & (ar['date'] <='2021-02')).astype(int)
#Creating dummy variable for 'trade war':
# 'tw1' = Obs. in Feb. 2018;
#Noted on timeline to be a time period of interest for 
    #U.S.-China trade negotiations, retaliation;
ar['tw2'] = ((ar['date'] >='2018-01') 
                             & (ar['date'] <='2018-02')).astype(int)

#COVID-19 Pandemic
#Creating a dummy variable for 'covid':
# 'covid' = Obs. in Mar. 2019 thru Feb. 2021;
#Noted to be a time period of interest;
ar['covid'] = ((ar['date'] >='2019-02') 
                             & (ar['date'] <='2021-02')).astype(int)


#"Example- 14-2 Extended v2 copy.py"
# For instructions for using all panel data methods see:
#   https://bashtage.github.io/linearmodels/doc/panel/models.html


# look at imported data:

# Find the summary statistics for all data 
Data_summary = ar.describe()
print('Articles Group:')
print(f'Data_summary:\n{Data_summary}\n')

# Find the correlation coeficients for all data 
Corr_coef = ar.corr()
print(f'Corr_coef:\n{Corr_coef}\n')



#Articles Group Estimation
#  dhts_() = Excl. dhts_3, dhts_9, dhts_12
#  d_id_() = Excl. d_id_4
# ddest_() = Excl. ddest_3

# FE model estimation:
reg = plm.PanelOLS.from_formula(formula='q ~ 1 +p + cpi + pop + exch'
                                '+dhts_10 + dhts_11'
                                '+ddest_1 +ddest_2 +ddest_4 +ddest_5'
                                '+tw1 +tw2 +covid'
                                '+EntityEffects'
                                ,data = ar, drop_absorbed=True)
results = reg.fit()

# print regression table:
table = pd.DataFrame({'b': round(results.params, 4),
                      'se': round(results.std_errors, 4),
                      't': round(results.tstats, 4),
                      'pval': round(results.pvalues, 4)})
print('Articles Group Estimation:')
print(f'table: \n{table}\n')
print(f'results.summary: \n{results.summary}\n')


print('Comparison of Pooled OLS, Random Effects & Fixed Effects')
print('Pooled OLS: Results')
reg_ols = plm.PooledOLS.from_formula(formula='q ~ 1+ p +cpi +gdp +pop +exch '                                                                         '+d_id_1 + d_id_2 +d_id_3 +d_id_5 '
                                     '+dhts_10 +dhts_11'
                                     '+d_id_1 +d_id_2 +d_id_3 +d_id_5'
                                     '+ddest_1 +ddest_2 +ddest_4 +ddest_5'
                                     '+tw1 +tw2 + covid'
                                     ,data = ar)
results_ols = reg_ols.fit()
print(f'results_ols.summary: \n{results_ols.summary}\n')

print('Articles Group Estimation:')
print('Random Effects: Results')
reg_re = plm.RandomEffects.from_formula(formula='q ~ 1+ p +cpi +gdp +pop +exch'                                       '+d_id_1 + d_id_2 +d_id_3 +d_id_5'
                                        '+dhts_10 +dhts_11'
                                        '+d_id_1 +d_id_2 +d_id_3 +d_id_5'
                                        '+ddest_1 +ddest_2 +ddest_4 +ddest_5'
                                        ,data = ar)
results_re = reg_re.fit()
print(f'results_re.summary: \n{results_re.summary}\n')

print('Articles Group Estimation:')
print('Fixed Effects: Results')
reg_fe = plm.PanelOLS.from_formula(formula='q ~ 1 +p + cpi + pop + exch'
                                '+dhts_10 +dhts_11'
                                '+ddest_1 +ddest_2 +ddest_4 +ddest_5'
                                '+tw1 +tw2 +covid'
                                '+EntityEffects'
                                ,data = ar, drop_absorbed=True)
results_fe = reg_fe.fit()
print(f'results_fe.summary: \n{results_fe.summary}\n')



