#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:34:15 2021

@author: andrew7
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 07:25:40 2021

@author: andrew7
"""

import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.stats.outliers_influence as smo

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

import numpy.linalg as la
from scipy import stats


###                      ANDREW LAMB (ID: 011442507)                       ###
###                      WASHINGTON STATE UNIVERSITY                       ###
###                      EconS 702 Research Project                        ###

#   Importing 'thre_RI.csv':
#Call brings in the following recorded observations for: 
#   Export quantities, values, derived price levels GDP, CPI, 
#   population, and exchange rates for the following countries:
#    United States, India, China, Japan, and Korea;
#For dates ranging:    
    #May 2009 thru (latest) Feb. 2021;
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
th = pd.read_csv('/Users/andrew7/'
                 'Desktop/[EconS702]/'
                 'DATA/'
                 'STACK/'
                 'panels_consolidated/'
                 'panel_stack/ready/'
                 'groups_files/'
                 'hs(__) + groups_files/'
                 'RI/(.csv files)/New RI/'
                 '-3/AppTex Thr_RI Drop -3.csv',
                 index_col = ['HTSCode', 'date'],
                 parse_dates =['date'])
#https://bashtage.github.io/linearmodels/devel/panel/examples/data-formats.html
th['date'] = pd.to_datetime(th[['year', 'month']].assign(DAY=1))

#Dropping any NaN values;
th.dropna(inplace=True)
#Dropping dummy variable for India (As a Country of Origin);
th = th.drop(['d_id_3'], axis =1)

#Printing the first few rows of each entity;
print(f'th.head(): \n{th.groupby("hscode").head()}\n')

#Generating Descriptive Statistics;
print(f'th.describe(): \n{th.describe()}\n')


#"Example- 14-2 Extended v2 copy.py"
# For instructions for using all panel data methods see:
#   https://bashtage.github.io/linearmodels/doc/panel/models.html


#Generating plot of Correlation Matrix;
corr = th.corr()
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right')




# Threads Group
# United States:
# Excl. = d_id_(2,3,4,5)
# Excl. = ddest_(1)
# Excl. = h_(_) 
#Using 'd_id_1' to indicate that we are specifying exports 
# originating from the United States;
th['u2c_t1'] = th.d_id_1 * th.h_2 *th.ddest_2 *th.tw1
th['u2i_t1'] = th.d_id_1 * th.h_2 *th.ddest_3 *th.tw1
th['u2j_t1'] = th.d_id_1 * th.h_2 *th.ddest_4 *th.tw1

th['u2c_t2'] = th.d_id_1 * th.h_2 *th.ddest_2 *th.tw2
th['u2i_t2'] = th.d_id_1 * th.h_2 *th.ddest_3 *th.tw2
th['u2j_t2'] = th.d_id_1 * th.h_2 *th.ddest_4 *th.tw2

th['u3c_t1'] = th.d_id_1 * th.h_3 *th.ddest_2 *th.tw1
th['u3i_t1'] = th.d_id_1 * th.h_3 *th.ddest_3 *th.tw1
th['u3j_t1'] = th.d_id_1 * th.h_3 *th.ddest_4 *th.tw1

th['u3c_t2'] = th.d_id_1 * th.h_3 *th.ddest_2 *th.tw2
th['u3i_t2'] = th.d_id_1 * th.h_3 *th.ddest_3 *th.tw2
th['u3j_t2'] = th.d_id_1 * th.h_3 *th.ddest_4 *th.tw2

th['uh2rpc19'] = th.d_id_1 * th.h_2 * th.rp_e * th.covid
th['uh3rpc19'] = th.d_id_1 * th.h_3 * th.rp_e * th.covid 


# FE model estimation:
print('Threads Group Estimation: United States')
print('Fixed Effects: Results')
reg_feu = plm.PanelOLS.from_formula(formula='q ~ d_id_1 +ddest_2 +ddest_3'
                                '+ddest_4 +h_2 +h_3 +tw1 +tw2 +covid'
                                '+h_4 +h_5 +h_6 +rp_e +gpc +exch'
                                '+u2c_t1 +u2i_t1 +u2j_t1'
                                '+u2c_t2 +u2i_t2 +u2j_t2'
                                '+u3c_t1 +u3i_t1 +u3j_t1'
                                '+u3c_t2 +u3i_t2 +u3j_t2'
                                '+uh2rpc19 +uh3rpc19'
                                  ,data = th, drop_absorbed=True) 
results_feu = reg_feu.fit(cov_type='robust', cluster_entity=True)
print(f'results_feu.summary: \n{results_feu.summary}\n')
print(f'Fixed Effects F-stat: \n{results_feu.f_statistic}\n')

# ## Calculate total sum of sqpcuares
# TSS = sum((qpc - np.mean(qpc))**2)

# ## Calculate residual sum of sqpcuares
# RSS = sum((results_feu.resids)**2)

# correct_rsq = 1 - (RSS / TSS)
# print(f'correct R^2: \n{correct_rsq}\n')

#FE Model Estimated Parameters
b_feu = results_feu.params
#print(f'FE Model Estimated Parameters: \n{b_fe}\n')

#fe Model Estimated Parameters Covariance
b_feu_cov = results_feu.cov
#print(f'FE Model Estimated Parameter Covariances: \n{b_fe_cov}\n')

# Store values for checking homoskedasticity graphically
fittedvals_feu = results_feu.predict().fitted_values
residuals_feu = results_feu.resids

# 3A. Homoskedasticity
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_feu, residuals_feu, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- FE Estimation'
             ' Threads Group, United States', fontsize = 12)
plt.show()


print('Threads Group Estimation: United States')
print('Pooled OLS: Results')
reg_olsu = plm.PooledOLS.from_formula(formula='q ~ 1+ d_id_1 +ddest_2 +ddest_3'
                                '+ddest_4 +h_2 +h_3 +tw1 +tw2 +covid'
                                '+h_4 +h_5 +h_6 +rp_e +gpc  +exch'
                                '+u2c_t1 +u2i_t1 +u2j_t1'
                                '+u2c_t2 +u2i_t2 +u2j_t2'
                                '+u3c_t1 +u3i_t1 +u3j_t1'
                                '+u3c_t2 +u3i_t2 +u3j_t2'
                                '+uh2rpc19 +uh3rpc19'                                
                                  ,data = th)
results_olsu = reg_olsu.fit(cov_type='robust', cluster_entity=True)
print(f'results_olsu.summary: \n{results_olsu.summary}\n')

# Store values for checking homoskedasticity graphically
fittedvals_pooled_OLSu = results_olsu.predict().fitted_values
residuals_pooled_OLSu = results_olsu.resids

# 3A. Homoskedasticity
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_pooled_OLSu, residuals_pooled_OLSu, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- PooledOLS Estimation'
             ' Threads Group, United States', fontsize = 12)
plt.show()

# 3A.2 White-Test
from statsmodels.stats.diagnostic import het_breuschpagan
pooled_OLSu_dataset = pd.concat([fittedvals_pooled_OLSu, residuals_pooled_OLSu], axis=1)
exog = sm.tools.tools.add_constant(pooled_OLSu_dataset).fillna(0)
# white_test_results = het_white(pooled_OLSu_dataset['residual'], exog)
# labels = ['LM-Stat', 'LM p-val', 'F-Stat', 'F p-val'] 
# print('White Test- Threads Group, United States')
# print(dict(zip(labels, white_test_results)))
# 3A.3 Breusch-Pagan-Test
breusch_pagan_test_results = het_breuschpagan(pooled_OLSu_dataset['residual'], exog)
labels = ['LM-Stat', 'LM p-val', 'F-Stat', 'F p-val'] 
print('Breusch-Pagan Test- Threads Group, United States')
print(dict(zip(labels, breusch_pagan_test_results)))

# 3.B Non-Autocorrelation
# Durbin-Watson-Test
from statsmodels.stats.stattools import durbin_watson

durbin_watson_test_results = durbin_watson(pooled_OLSu_dataset['residual']) 
print(f'Durbin-Watson Test results- Threads Group, United States: \n{durbin_watson_test_results}\n')


print('Threads Group Estimation: United States')
print('Random Effects: Results')
reg_reu = plm.RandomEffects.from_formula(formula='q ~ 1+ d_id_1 +ddest_2 +ddest_3'
                                '+ddest_4 +h_2 +h_3 +tw1 +tw2 +covid'
                                '+h_4 +h_5 +h_6 +rp_e +gpc +exch'
                                '+u2c_t1 +u2i_t1 +u2j_t1'
                                '+u2c_t2 +u2i_t2 +u2j_t2'
                                '+u3c_t1 +u3i_t1 +u3j_t1'
                                '+u3c_t2 +u3i_t2 +u3j_t2'
                                '+uh2rpc19 +uh3rpc19'
                                   ,data = th)
results_reu = reg_reu.fit(cov_type='robust', cluster_entity=True)
print(f'results_reu.summary: \n{results_reu.summary}\n')
# ## Calculate total sum of sqpcuares
# TSS = sum((qpc - np.mean(qpc))**2)

# ## Calculate residual sum of sqpcuares
# RSS = sum((results_reu.resids)**2)

# correct_rsq = 1 - (RSS / TSS)
# print(f'correct R^2: \n{correct_rsq}\n')

#RE Model Estimated Parameters
b_reu = results_reu.params
#print(f'RE Model Estimated Parameters: \n{b_re}\n')

#RE Model Estimated Parameters Covariance
b_reu_cov = results_reu.cov
#print(f'RE Model Estimated Parameter Covariances: \n{b_re_cov}\n')

# Store values for checking homoskedasticity graphically
fittedvals_reu = results_reu.predict().fitted_values
residuals_reu = results_reu.resids

# 3A. Homoskedasticity
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_reu, residuals_reu, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- RE Estimation'
             ' Threads Group, United States', fontsize = 12)
plt.show()


# Hausman test of FE vs. RE
# (I) find overlapping coefficients:
common_coef = set(results_feu.params.index).intersection(results_reu.params.index)

# (II) calculate differences between FE and RE:
b_diff = np.array(results_feu.params[common_coef] - results_reu.params[common_coef])
df = len(b_diff)
b_diff.reshape((df, 1))
b_cov_diff = np.array(b_feu_cov.loc[common_coef, common_coef] -
                      b_reu_cov.loc[common_coef, common_coef])
b_cov_diff.reshape((df, df))

# (III) calculate test statistic:
stat = abs(np.transpose(b_diff) @ np.linalg.inv(b_cov_diff) @ b_diff)
pval = 1 - stats.chi2.cdf(stat, df)
print('Hausman Results():')
print(f'stat: {stat}\n')
print(f'pval: {pval}\n')

# Threads Group
# China:
# Excl. = d_id_(1,3,4,5)
# Excl. = ddest_(2)
# Excl. = h_(_) 
th['c2u_t1'] = th.d_id_2 * th.h_2 *th.ddest_1 *th.tw1
th['c2i_t1'] = th.d_id_2 * th.h_2 *th.ddest_3 *th.tw1
th['c2j_t1'] = th.d_id_2 * th.h_2 *th.ddest_4 *th.tw1

th['c2u_t2'] = th.d_id_2 * th.h_2 *th.ddest_1 *th.tw2
th['c2i_t2'] = th.d_id_2 * th.h_2 *th.ddest_3 *th.tw2
th['c2j_t2'] = th.d_id_2 * th.h_2 *th.ddest_4 *th.tw2

th['c3u_t1'] = th.d_id_2 * th.h_3 *th.ddest_1 *th.tw1
th['c3i_t1'] = th.d_id_2 * th.h_3 *th.ddest_3 *th.tw1
th['c3j_t1'] = th.d_id_2 * th.h_3 *th.ddest_4 *th.tw1

th['c3u_t2'] = th.d_id_2 * th.h_3 *th.ddest_1 *th.tw2
th['c3i_t2'] = th.d_id_2 * th.h_3 *th.ddest_3 *th.tw2
th['c3j_t2'] = th.d_id_2 * th.h_3 *th.ddest_4 *th.tw2

th['ch2rpc19'] = th.d_id_2 * th.h_2 * th.rp_e * th.covid
th['ch3rpc19'] = th.d_id_2 * th.h_3 * th.rp_e * th.covid 


#Using 'd_id_2' to indicate that we are specifying exports 
# originating from China;
# FE model estimation:
print('Threads Group Estimation: China')
print('Fixed Effects: Results')
reg_fec = plm.PanelOLS.from_formula(formula='q ~ d_id_2 +ddest_1 +ddest_3'
                                '+ddest_4 +h_2 +h_3'
                                '+h_4 +h_5 +h_6 +rp_e +gpc +exch'
                                '+tw1 +tw2 +covid'
                                '+c2u_t1 +c2i_t1 +c2j_t1'
                                '+c2u_t2 +c2i_t2 +c2j_t2'
                                '+c3u_t1 +c3i_t1 +c3j_t1'
                                '+c3u_t2 +c3i_t2 +c3j_t2'
                                '+ch2rpc19 +ch3rpc19'
                                ,data = th, drop_absorbed=True)
results_fec = reg_fec.fit(cov_type='robust', cluster_entity=True)
print(f'results_fec.summary: \n{results_fec.summary}\n')
print(f'Fixed Effects F-stat: \n{results_fec.f_statistic}\n')

# ## Calculate total sum of sqpcuares
# TSS = sum((qpc - np.mean(qpc))**2)

# ## Calculate residual sum of sqpcuares
# RSS = sum((results_fec.resids)**2)

# correct_rsq = 1 - (RSS / TSS)
# print(f'correct R^2: \n{correct_rsq}\n')

#FE Model Estimated Parameters
b_fec = results_fec.params
#print(f'FE Model Estimated Parameters: \n{b_fe}\n')

#fe Model Estimated Parameters Covariance
b_fec_cov = results_fec.cov
#print(f'FE Model Estimated Parameter Covariances: \n{b_fe_cov}\n')

# Store values for checking homoskedasticity graphically
fittedvals_fec = results_fec.predict().fitted_values
residuals_fec = results_fec.resids

# 3A. Homoskedasticity
import matplotlib.pyplot as plt
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_fec, residuals_fec, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- FE Estimation'
             ' Threads Group, China', fontsize = 12)
plt.show()


print('Threads Group Estimation: China')
print('Pooled OLS: Results')
reg_olsc = plm.PooledOLS.from_formula(formula='q ~ 1+ d_id_2 +ddest_1 +ddest_3'
                                '+ddest_4 +h_2 +h_3'
                                '+h_4 +h_5 +h_6 +rp_e +gpc  +exch'
                                '+tw1 +tw2 +covid'
                                '+c2u_t1 +c2i_t1 +c2j_t1'
                                '+c2u_t2 +c2i_t2 +c2j_t2'
                                '+c3u_t1 +c3i_t1 +c3j_t1'
                                '+c3u_t2 +c3i_t2 +c3j_t2'
                                '+ch2rpc19 +ch3rpc19'
                                ,data = th)
results_olsc = reg_olsc.fit(cov_type='robust', cluster_entity=True)
print(f'results_olsc.summary: \n{results_olsc.summary}\n')

# Store values for checking homoskedasticity graphically
fittedvals_pooled_OLSc = results_olsc.predict().fitted_values
residuals_pooled_OLSc = results_olsc.resids

# 3A. Homoskedasticity
import matplotlib.pyplot as plt
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_pooled_OLSc, residuals_pooled_OLSc, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- PooledOLS Estimation'
             ' Threads Group, China', fontsize = 12)
plt.show()

# 3A.2 White-Test
from statsmodels.stats.diagnostic import het_breuschpagan
pooled_OLSc_dataset = pd.concat([fittedvals_pooled_OLSc, residuals_pooled_OLSc], axis=1)
exog = sm.tools.tools.add_constant(pooled_OLSc_dataset).fillna(0)
# white_test_results = het_white(pooled_OLSc_dataset['residual'], exog)
# labels = ['LM-Stat', 'LM p-val', 'F-Stat', 'F p-val'] 
# print('White Test- PooledOLS: Threads Group, China')
# print(dict(zip(labels, white_test_results)))
# 3A.3 Breusch-Pagan-Test
breusch_pagan_test_results = het_breuschpagan(pooled_OLSc_dataset['residual'], exog)
labels = ['LM-Stat', 'LM p-val', 'F-Stat', 'F p-val'] 
print('Breusch-Pagan Test- PooledOLS: Threads Group, China')
print(dict(zip(labels, breusch_pagan_test_results)))

# 3.B Non-Autocorrelation
# Durbin-Watson-Test
from statsmodels.stats.stattools import durbin_watson

durbin_watson_test_results = durbin_watson(pooled_OLSc_dataset['residual']) 
print(f'Durbin-Watson Test results- Threads Group, China: \n{durbin_watson_test_results}\n')


print('Threads Group Estimation: China')
print('Random Effects: Results')
reg_rec = plm.RandomEffects.from_formula(formula='q ~ 1+ d_id_2 +ddest_1 +ddest_3'
                                '+ddest_4 +h_2 +h_3'
                                '+h_4 +h_5 +h_6 +rp_e +gpc  +exch'
                                '+tw1 +tw2 +covid'
                                '+c2u_t1 +c2i_t1 +c2j_t1'
                                '+c2u_t2 +c2i_t2 +c2j_t2'
                                '+c3u_t1 +c3i_t1 +c3j_t1'
                                '+c3u_t2 +c3i_t2 +c3j_t2'
                                '+ch2rpc19 +ch3rpc19'
                                ,data = th)
results_rec = reg_rec.fit(cov_type='robust', cluster_entity=True)
print(f'results_rec.summary: \n{results_rec.summary}\n')
print(f'Random Effects F-stat: \n{results_rec.f_statistic}\n')

# ## Calculate total sum of sqpcuares
# TSS = sum((qpc - np.mean(qpc))**2)

# ## Calculate residual sum of sqpcuares
# RSS = sum((results_rec.resids)**2)

# correct_rsq = 1 - (RSS / TSS)
# print(f'correct R^2: \n{correct_rsq}\n')

#RE Model Estimated Parameters
b_rec = results_rec.params
#print(f'RE Model Estimated Parameters: \n{b_re}\n')

#RE Model Estimated Parameters Covariance
b_rec_cov = results_rec.cov
#print(f'RE Model Estimated Parameter Covariances: \n{b_re_cov}\n')

# Store values for checking homoskedasticity graphically
fittedvals_rec = results_rec.predict().fitted_values
residuals_rec = results_rec.resids

# 3A. Homoskedasticity
import matplotlib.pyplot as plt
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_rec, residuals_rec, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- RE Estimation'
             ' Threads Group, China', fontsize = 12)
plt.show()


# Hausman test of FE vs. RE
# (I) find overlapping coefficients:
common_coef = set(results_fec.params.index).intersection(results_rec.params.index)

# (II) calculate differences between FE and RE:
b_diff = np.array(results_fec.params[common_coef] - results_rec.params[common_coef])
df = len(b_diff)
b_diff.reshape((df, 1))
b_cov_diff = np.array(b_fec_cov.loc[common_coef, common_coef] -
                      b_rec_cov.loc[common_coef, common_coef])
b_cov_diff.reshape((df, df))

# (III) calculate test statistic:
stat = abs(np.transpose(b_diff) @ np.linalg.inv(b_cov_diff) @ b_diff)
pval = 1 - stats.chi2.cdf(stat, df)
print('Hausman Results():')
print(f'stat: {stat}\n')
print(f'pval: {pval}\n')


# Threads Group
# Japan:
# Excl. = d_id_(1,2,3,5)
# Excl. = ddest_(4)
# Excl. = h_(_) 
th['j2u_t1'] = th.d_id_4 * th.h_2 *th.ddest_1 *th.tw1
th['j2c_t1'] = th.d_id_4 * th.h_2 *th.ddest_2 *th.tw1
th['j2k_t1'] = th.d_id_4 * th.h_2 *th.ddest_5 *th.tw1

th['j2u_t2'] = th.d_id_4 * th.h_2 *th.ddest_1 *th.tw2
th['j2c_t2'] = th.d_id_4 * th.h_2 *th.ddest_2 *th.tw2
th['j2k_t2'] = th.d_id_4 * th.h_2 *th.ddest_5 *th.tw2

th['j3u_t1'] = th.d_id_4 * th.h_3 *th.ddest_1 *th.tw1
th['j3c_t1'] = th.d_id_4 * th.h_3 *th.ddest_2 *th.tw1
th['j3k_t1'] = th.d_id_4 * th.h_3 *th.ddest_5 *th.tw1

th['j3u_t2'] = th.d_id_4 * th.h_3 *th.ddest_1 *th.tw2
th['j3c_t2'] = th.d_id_4 * th.h_3 *th.ddest_2 *th.tw2
th['j3k_t2'] = th.d_id_4 * th.h_3 *th.ddest_5 *th.tw2

th['jh2rpc19'] = th.d_id_4 * th.h_2 * th.rp_e * th.covid
th['jh3rpc19'] = th.d_id_4 * th.h_3 * th.rp_e * th.covid 


#Using 'd_id_4' to indicate that we are specifying exports 
# originating from Japan;
# FE model estimation:
print('Threads Group Estimation: Japan')
print('Fixed Effects: Results')
reg_fej = plm.PanelOLS.from_formula(formula='q ~ d_id_4 +ddest_1 +ddest_2'
                                ' +ddest_5 +h_2 +h_3'
                                '+h_4 +h_5 +h_6 +rp_e +gpc  +exch'
                                '+j2u_t1 +j2c_t1 +j2k_t1'
                                '+j2u_t2 +j2c_t2 +j2k_t2'
                                '+j3u_t1 +j3c_t1 +j3k_t1'
                                '+j3u_t2 +j3c_t2 +j3k_t2'
                                '+jh2rpc19 +jh3rpc19'
                                ,data = th, drop_absorbed=True) 
results_fej = reg_fej.fit(cov_type='robust', cluster_entity=True)
print(f'results_fej.summary: \n{results_fej.summary}\n')
print(f'Fixed Effects F-stat: \n{results_fej.f_statistic}\n')

# ## Calculate total sum of sqpcuares
# TSS = sum((qpc - np.mean(qpc))**2)

# ## Calculate residual sum of sqpcuares
# RSS = sum((results_fej.resids)**2)

# correct_rsq = 1 - (RSS / TSS)
# print(f'correct R^2: \n{correct_rsq}\n')

#FE Model Estimated Parameters
b_fej = results_fej.params
#print(f'FE Model Estimated Parameters: \n{b_fe}\n')

#fe Model Estimated Parameters Covariance
b_fej_cov = results_fej.cov
#print(f'FE Model Estimated Parameter Covariances: \n{b_fe_cov}\n')

# Store values for checking homoskedasticity graphically
fittedvals_fej = results_fej.predict().fitted_values
residuals_fej = results_fej.resids

# 3A. Homoskedasticity
import matplotlib.pyplot as plt
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_fej, residuals_fej, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- FE Estimation'
             ' Threads Group, Japan', fontsize = 12)
plt.show()


print('Threads Group Estimation: Japan')
print('Pooled OLS: Results')
reg_olsj = plm.PooledOLS.from_formula(formula='q ~ 1+ d_id_4 +ddest_1 +ddest_2'
                                ' +ddest_5 +h_2 +h_3'
                                '+h_4 +h_5 +h_6 +rp_e +gpc  +exch'
                                '+j2u_t1 +j2c_t1 +j2k_t1'
                                '+j2u_t2 +j2c_t2 +j2k_t2'
                                '+j3u_t1 +j3c_t1 +j3k_t1'
                                '+j3u_t2 +j3c_t2 +j3k_t2'
                                '+jh2rpc19 +jh3rpc19'
                                ,data = th)
results_olsj = reg_olsj.fit(cov_type='robust', cluster_entity=True)
print(f'results_olsj.summary: \n{results_olsj.summary}\n')

# Store values for checking homoskedasticity graphically
fittedvals_pooled_OLSj = results_olsj.predict().fitted_values
residuals_pooled_OLSj = results_olsj.resids

# 3A. Homoskedasticity
import matplotlib.pyplot as plt
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_pooled_OLSj, residuals_pooled_OLSj, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- PooledOLS Estimation'
             ' Threads Group, Japan', fontsize = 12)
plt.show()

# 3A.2 White-Test
from statsmodels.stats.diagnostic import het_breuschpagan
pooled_OLSj_dataset = pd.concat([fittedvals_pooled_OLSj, residuals_pooled_OLSj], axis=1)
exog = sm.tools.tools.add_constant(pooled_OLSj_dataset).fillna(0)
# white_test_results = het_white(pooled_OLSj_dataset['residual'], exog)
# labels = ['LM-Stat', 'LM p-val', 'F-Stat', 'F p-val'] 
# print('White Test- PooledOLS: Fabrics Group, Japan')
# print(dict(zip(labels, white_test_results)))
# 3A.3 Breusch-Pagan-Test
breusch_pagan_test_results = het_breuschpagan(pooled_OLSj_dataset['residual'], exog)
labels = ['LM-Stat', 'LM p-val', 'F-Stat', 'F p-val'] 
print('Breusch-Pagan Test- PooledOLS: Threads Group, Japan')
print(dict(zip(labels, breusch_pagan_test_results)))


# 3.B Non-Autocorrelation
# Durbin-Watson-Test
from statsmodels.stats.stattools import durbin_watson

durbin_watson_test_results = durbin_watson(pooled_OLSj_dataset['residual']) 
print(f'Durbin-Watson Test results- Threads Group, Japan: \n{durbin_watson_test_results}\n')


print('Threads Group Estimation: Japan')
print('Random Effects: Results')
reg_rej = plm.RandomEffects.from_formula(formula='q ~ 1+ d_id_4 +ddest_1 +ddest_2'
                                ' +ddest_5 +h_2 +h_3'
                                '+h_4 +h_5 +h_6 +rp_e +gpc  +exch'
                                '+j2u_t1 +j2c_t1 +j2k_t1'
                                '+j2u_t2 +j2c_t2 +j2k_t2'
                                '+j3u_t1 +j3c_t1 +j3k_t1'
                                '+j3u_t2 +j3c_t2 +j3k_t2'
                                '+jh2rpc19 +jh3rpc19'
                                ,data = th)
results_rej = reg_rej.fit(cov_type='robust', cluster_entity=True)
print(f'results_rej.summary: \n{results_rej.summary}\n')
print(f'Random Effects F-stat: \n{results_rej.f_statistic}\n')

# ## Calculate total sum of sqpcuares
# TSS = sum((qpc - np.mean(qpc))**2)

# ## Calculate residual sum of sqpcuares
# RSS = sum((results_rej.resids)**2)

# correct_rsq = 1 - (RSS / TSS)
# print(f'correct R^2: \n{correct_rsq}\n')

#RE Model Estimated Parameters
b_rej = results_rej.params
#print(f'RE Model Estimated Parameters: \n{b_re}\n')

#RE Model Estimated Parameters Covariance
b_rej_cov = results_rej.cov
#print(f'RE Model Estimated Parameter Covariances: \n{b_re_cov}\n')

# Store values for checking homoskedasticity graphically
fittedvals_rej = results_rej.predict().fitted_values
residuals_rej = results_rej.resids

# 3A. Homoskedasticity
import matplotlib.pyplot as plt
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_rej, residuals_rej, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- RE Estimation'
             ' Threads Group, Japan', fontsize = 12)
plt.show()

# Hausman test of FE vs. RE
# (I) find overlapping coefficients:
common_coef = set(results_fej.params.index).intersection(results_rej.params.index)

# (II) calculate differences between FE and RE:
b_diff = np.array(results_fej.params[common_coef] - results_rej.params[common_coef])
df = len(b_diff)
b_diff.reshape((df, 1))
b_cov_diff = np.array(b_fej_cov.loc[common_coef, common_coef] -
                      b_rej_cov.loc[common_coef, common_coef])
b_cov_diff.reshape((df, df))

# (III) calculate test statistic:
stat = abs(np.transpose(b_diff) @ np.linalg.inv(b_cov_diff) @ b_diff)
pval = 1 - stats.chi2.cdf(stat, df)
print('Hausman Results():')
print(f'stat: {stat}\n')
print(f'pval: {pval}\n')

# Threads Group
# Korea:
# Excl. = d_id_(1,2,3,4)
# Excl. = ddest_(4)
# Excl. = h_(_) 
th['k2u_t1'] = th.d_id_5 * th.h_2 *th.ddest_1 *th.tw1
th['k2c_t1'] = th.d_id_5 * th.h_2 *th.ddest_2 *th.tw1
th['k2j_t1'] = th.d_id_5 * th.h_2 *th.ddest_4 *th.tw1

th['k2u_t2'] = th.d_id_5 * th.h_2 *th.ddest_1 *th.tw2
th['k2c_t2'] = th.d_id_5 * th.h_2 *th.ddest_2 *th.tw2
th['k2j_t2'] = th.d_id_5 * th.h_2 *th.ddest_4 *th.tw2

th['k3u_t1'] = th.d_id_5 * th.h_3 *th.ddest_1 *th.tw1
th['k3c_t1'] = th.d_id_5 * th.h_3 *th.ddest_2 *th.tw1
th['k3j_t1'] = th.d_id_5 * th.h_3 *th.ddest_4 *th.tw1

th['k3u_t2'] = th.d_id_5 * th.h_3 *th.ddest_1 *th.tw2
th['k3c_t2'] = th.d_id_5 * th.h_3 *th.ddest_2 *th.tw2
th['k3j_t2'] = th.d_id_5 * th.h_3 *th.ddest_4 *th.tw2

th['kh2rpc19'] = th.d_id_5 * th.h_2 * th.rp_e * th.covid
th['kh3rpc19'] = th.d_id_5 * th.h_3 * th.rp_e * th.covid 

#Using 'd_id_5' to indicate that we are specifying exports 
# originating from Korea;
# FE model estimation:
print('Threads Group Estimation: Korea')
print('Fixed Effects: Results')
reg_fek = plm.PanelOLS.from_formula(formula='q ~ d_id_5 +ddest_1 +ddest_2'
                                '+ddest_3 +ddest_4 +h_2 +h_3'
                                '+h_4 +h_5 +h_6 +rp_e +gpc +exch'
                                '+tw1 +tw2 +covid'
                                '+k2u_t1 +k2c_t1 +k2j_t1'
                                '+k2u_t2 +k2c_t2 +k2j_t2'
                                '+k3u_t1 +k3c_t1 +k3j_t1'
                                '+k3u_t2 +k3c_t2 +k3j_t2'
                                '+kh2rpc19 +kh3rpc19'
                                ,data = th, drop_absorbed=True) 
results_fek = reg_fek.fit(cov_type='robust', cluster_entity=True)
print(f'results_fek.summary: \n{results_fek.summary}\n')
print(f'Fixed Effects F-stat: \n{results_fek.f_statistic}\n')

# ## Calculate total sum of sqpcuares
# TSS = sum((qpc - np.mean(qpc))**2)

# ## Calculate residual sum of sqpcuares
# RSS = sum((results_fek.resids)**2)

# correct_rsq = 1 - (RSS / TSS)
# print(f'correct R^2: \n{correct_rsq}\n')

#FE Model Estimated Parameters
b_fek = results_fek.params
#print(f'FE Model Estimated Parameters: \n{b_fe}\n')

#fe Model Estimated Parameters Covariance
b_fek_cov = results_fek.cov
#print(f'FE Model Estimated Parameter Covariances: \n{b_fe_cov}\n')

# Store values for checking homoskedasticity graphically
fittedvals_fek = results_fek.predict().fitted_values
residuals_fek = results_fek.resids

# 3A. Homoskedasticity
import matplotlib.pyplot as plt
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_fek, residuals_fek, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- FE Estimation'
             ' Threads Group, Korea', fontsize = 12)
plt.show()


print('Threads Group Estimation: Korea')
print('Pooled OLS: Results')
reg_olsk = plm.PooledOLS.from_formula(formula='q ~ 1+ d_id_5 +ddest_1 +ddest_2'
                                '+ddest_3 +ddest_4 +h_2 +h_3'
                                '+h_4 +h_5 +h_6 +rp_e +gpc +exch'
                                '+tw1 +tw2 +covid'
                                '+k2u_t1 +k2c_t1 +k2j_t1'
                                '+k2u_t2 +k2c_t2 +k2j_t2'
                                '+k3u_t1 +k3c_t1 +k3j_t1'
                                '+k3u_t2 +k3c_t2 +k3j_t2'
                                '+kh2rpc19 +kh3rpc19'
                                ,data = th)
results_olsk = reg_olsk.fit(cov_type='robust', cluster_entity=True)
print(f'results_olsk.summary: \n{results_olsk.summary}\n')

# Store values for checking homoskedasticity graphically
fittedvals_pooled_OLSk = results_olsk.predict().fitted_values
residuals_pooled_OLSk = results_olsk.resids

# 3A. Homoskedasticity
import matplotlib.pyplot as plt
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_pooled_OLSk, residuals_pooled_OLSk, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- PooledOLS Estimation'
             ' Threads Group, Korea', fontsize = 12)
plt.show()

# 3A.2 White-Test
from statsmodels.stats.diagnostic import het_breuschpagan
pooled_OLSk_dataset = pd.concat([fittedvals_pooled_OLSk, residuals_pooled_OLSk], axis=1)

exog = sm.tools.tools.add_constant(pooled_OLSk_dataset).fillna(0)
# white_test_results = het_white(pooled_OLSk_dataset['residual'], exog)
# labels = ['LM-Stat', 'LM p-val', 'F-Stat', 'F p-val'] 
# print('White Test- PooledOLS: Threads Group, Korea')
# print(dict(zip(labels, white_test_results)))
# 3A.3 Breusch-Pagan-Test
breusch_pagan_test_results = het_breuschpagan(pooled_OLSk_dataset['residual'], exog)
labels = ['LM-Stat', 'LM p-val', 'F-Stat', 'F p-val'] 
print('Breusch-Pagan Test- PooledOLS: Threads Group, Korea')
print(dict(zip(labels, breusch_pagan_test_results)))


# 3.B Non-Autocorrelation
# Durbin-Watson-Test
from statsmodels.stats.stattools import durbin_watson

durbin_watson_test_results = durbin_watson(pooled_OLSk_dataset['residual']) 
print(f'Durbin-Watson Test results- Threads Group, Korea: \n{durbin_watson_test_results}\n')


print('Threads Group Estimation: Korea')
print('Random Effects: Results')
reg_rek = plm.RandomEffects.from_formula(formula='q ~ 1+ d_id_5 +ddest_1 +ddest_2'
                                '+ddest_3 +ddest_4 +h_2 +h_3'
                                '+h_4 +h_5 +h_6 +rp_e +gpc +exch'
                                '+tw1 +tw2 +covid'
                                '+k2u_t1 +k2c_t1 +k2j_t1'
                                '+k2u_t2 +k2c_t2 +k2j_t2'
                                '+k3u_t1 +k3c_t1 +k3j_t1'
                                '+k3u_t2 +k3c_t2 +k3j_t2'
                                '+kh2rpc19 +kh3rpc19'
                                ,data = th)
results_rek = reg_rek.fit(cov_type='robust', cluster_entity=True)
print(f'results_rek.summary: \n{results_rek.summary}\n')
print(f'Random Effects F-stat: \n{results_rek.f_statistic}\n')

# ## Calculate total sum of sqpcuares
# TSS = sum((qpc - np.mean(qpc))**2)

# ## Calculate residual sum of sqpcuares
# RSS = sum((results_rek.resids)**2)

# correct_rsq = 1 - (RSS / TSS)
# print(f'correct R^2: \n{correct_rsq}\n')

#RE Model Estimated Parameters
b_rek = results_rek.params
#print(f'RE Model Estimated Parameters: \n{b_re}\n')

#RE Model Estimated Parameters Covariance
b_rek_cov = results_rek.cov
#print(f'RE Model Estimated Parameter Covariances: \n{b_re_cov}\n')

# Store values for checking homoskedasticity graphically
fittedvals_rek = results_rek.predict().fitted_values
residuals_rek = results_rek.resids

# 3A. Homoskedasticity
import matplotlib.pyplot as plt
 # 3A.1 Residuals-Plot for growing Variance Detection
fig, ax = plt.subplots()
ax.scatter(fittedvals_rek, residuals_rek, color = 'blue')
ax.axhline(0,color = 'r', ls = '--')
ax.set_xlabel('Predicted Values', fontsize = 15)
ax.set_ylabel('Residuals', fontsize = 15)
ax.set_title('Homoskedasticity Test- RE Estimation'
             ' Threads Group, Korea', fontsize = 12)
plt.show()


# Hausman test of FE vs. RE
# (I) find overlapping coefficients:
common_coef = set(results_fek.params.index).intersection(results_rek.params.index)

# (II) calculate differences between FE and RE:
b_diff = np.array(results_fek.params[common_coef] - results_rek.params[common_coef])
df = len(b_diff)
b_diff.reshape((df, 1))
b_cov_diff = np.array(b_fek_cov.loc[common_coef, common_coef] -
                      b_rek_cov.loc[common_coef, common_coef])
b_cov_diff.reshape((df, df))

# (III) calculate test statistic:
stat = abs(np.transpose(b_diff) @ np.linalg.inv(b_cov_diff) @ b_diff)
pval = 1 - stats.chi2.cdf(stat, df)
print('Hausman Results():')
print(f'stat: {stat}\n')
print(f'pval: {pval}\n')

