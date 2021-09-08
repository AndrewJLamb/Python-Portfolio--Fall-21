#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 12:59:28 2021

@author: andrew7
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 13:47:29 2021

@author: andrew7
"""

import numpy as np
import statsmodels.api as sm
import statsmodels.stats.outliers_influence as smo
import pandas as pd 
import matplotlib.pyplot as plt


#Andrew Lamb
#Econ S426 Project;
#Python output (To be attached);
#Import Traffic_accident.xlsx;
df = pd.read_excel("/Users/andrew7/Desktop/Traffic_accident.xlsx") 

#Creating Dummy Variable for Accident, Gender, Vehicle types;
df['Accident_d'] = (df['Accident'] == 'Yes').astype(int)                  # False=0, True=1
df['Gender_d'] = (df['Gender'] == 'Male').astype(int)                     # False=0, True=1
df['Type_SUV'] = (df['Vehicle_Type'] == 'SUV').astype(int)                # False=0, True=1
df['Type_Sedan'] = (df['Vehicle_Type'] == 'Sedan').astype(int)            # False=0, True=1
df['Type_Motorcycle'] = (df['Vehicle_Type'] == 'Motorcycle').astype(int)  # False=0, True=1
df['Type_Truck'] = (df['Vehicle_Type'] == 'Truck').astype(int)            # False=0, True=1
with pd.option_context('display.max_columns', 30):
    print(df)
    
#Descriptive Statistics:
Data_summary = df.describe()
with pd.option_context('display.max_columns', 30):
    print(f'Data_summary:\n{Data_summary}\n')

#Defining independent, dependent variables;
X1 = df[['Age_Driver', 'Gender_d','Household_Income',
        'Type_SUV','Type_Sedan','Type_Motorcycle', 
        'Type_Truck','Insurance_Premium', 'Age_Car_Months']]
y1 = df['Accident_d']

#Running Logit regression;
log_reg1 = sm.Logit(y1, X1).fit(disp=0)

#Logit regression summary table;
print(log_reg1.summary())

#VIF's for Logit(y1, X1);
K1 = X1.shape[1]
VIF = np.empty(K1)
for i in range(K1):
    VIF[i] = smo.variance_inflation_factor(X1.values, i)
print(f'VIF(Model): \n{VIF}\n')      #High VIF's; Dropping one of the 'Vehicle_Type' var.'s


#Test model w/ 'Type_Truck' omitted;
X2 = df[['Age_Driver', 'Gender_d','Household_Income',
        'Type_SUV','Type_Sedan','Type_Motorcycle', 
        'Insurance_Premium', 'Age_Car_Months']]
y2 = df['Accident_d']

#Running Logit regression;
#Defining independent, dependent variables;
log_reg2 = sm.Logit(y2, X2).fit(disp=0)

#Logit regression summary table;
print(log_reg2.summary())

#VIF's for Logit(y2, X2);
K2 = X2.shape[1]
VIF = np.empty(K2)
for i in range(K2):
    VIF[i] = smo.variance_inflation_factor(X2.values, i)
print(f'VIF(Model): \n{VIF}\n')

#Performing predictions on the 2nd Model;
yhat2 = log_reg2.predict(X2)
prediction = list(map(round, yhat2))

#Importing sklearn for confusion matrix; 
from sklearn.metrics import (confusion_matrix, 
                           accuracy_score)
#Creating confusion matrix to text predictive power of our Accidents model;
cm = confusion_matrix(y2, prediction) 
print ("\nConfusion Matrix:\n", cm) 

#Accuracy score of the model
print('Test accuracy= \n', accuracy_score(y2, prediction))


#Creating Confusion Matrix Figure;
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(cm)
ax.grid(False)
ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
ax.set_ylim(1.5, -0.5)
for i in range(2):
    for j in range(2):
        ax.text(j, i, cm[i, j], ha='center', va='center', color='black')
plt.show()





