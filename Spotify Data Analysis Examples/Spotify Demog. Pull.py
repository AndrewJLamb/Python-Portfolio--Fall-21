#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:16:36 2021

@author: andrew7
"""





import numpy as np 
import pandas as pd 
import xlsxwriter as ExcelWriter
import statsmodels.formula.api as smf
import statsmodels as sm 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import seaborn as sns
from pandas.plotting import register_matplotlib_converters # Handle date-time 
register_matplotlib_converters()                           #conversions between
                                                           #pandas and matplotlib

###                      EWOP STUDIOS                                      ###
###    DATA ANALYSIS on : TONE SINATRA, SPOTIFY for ARTISTS RAW DATA       ###
###           BY: ANDREW LAMB, LAURENCE HICKS                              ###
###    (QUESTIONS OR CONCERNS? Email: andrew@ewopstudios.com)              ###
                                                           
#Importing TIMELINES04162020thru05172021:
    #(The .csv output from Spotify for Artists webpage)
#Call brings in the following recorded observations for the 
#date; followers; listeners; streams for 
    #April 16th, 2020 thru May 17th, 2021;
#Import csv data file. Return type from function is a pandas DataFrame;
tl = pd.read_excel('/Users/'
                     'andrew7/'
                     'Desktop/'
                     '[TONE_DA]/'
                     '[SPOTIFY_py]/'
                     '(.xlsx, .csv) files/'
                     'TIMELINES04162020THRU05172021.xlsx')
#Use pd.set_option to print all rows and columns;
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(f'tl.head(): \n{tl.head()}\n')     #Checking the first and last few rows                            
print(f'tl.tail(): \n{tl.tail()}\n')     #of TIMELINES04162020thru05172021


#Working out demog. as rough time-series estimate 
#[Demog.] gender %'s (rough, 5/17/2021 collection date)
#Percentages accessed from 'Audience' tab
    #https://artists.spotify.com/c/artist/1xDlocsrJxyAogaOvuV6HJ/audience;
        #Listeners = Total listeners worldwide;
    #Formula= (Total listeners)*(Gender spec.'s share of listeners as a %)
#NOTE: "lg(x)" = Listener gender group(x):
    #(x=1) = Male identifying listeners;
    #(x=2) = Female identifying listeners;   
    #(x=3) = Non-Binary identifying listeners;
#[Demog.] Male identifying listeners
tl['lg1'] = tl['listeners'].astype('int32')  #(as a % of total listeners);
tl['lg2'] = (tl['listeners']
                 * 0.84).astype('int32')          #Male= ~84%;

#[Demog.] Female identifying listeners
# (as a % of total listeners)
tl['lg2'] = tl['listeners'].astype('int32')  #(as a % of total listeners);
tl['lg2'] = (tl['listeners'] 
                 * 0.13).astype('int32')          #Female= ~13%;

#[Demog.] Non-binary identifying listeners
# (as a % of total listeners)
tl['lg3'] = tl['listeners'].astype('int32') #(as a % of total listeners);
tl['lg3'] = (tl['listeners'] 
                  * 0.02).astype('int32')         #NB= ~2%;

#Rounding the above derived values to whole numbers;
round(tl.lg1, 0)
round(tl.lg2, 0)
round(tl.lg3, 0)


#Working out demog. as rough time-series estimate 
#[Demog.] age group %'s (rough, 5/17/2021 collection date)
#Percentages accessed from 'Audience' tab
    #https://artists.spotify.com/c/artist/1xDlocsrJxyAogaOvuV6HJ/audience;
        #Listeners = Total listeners worldwide;
        #Age group's share of listeners = Percentage value
    #Formula= (Total listeners)*(Age group's share of listeners as a %)
#[Demog.] Listeners by age group
    # (Specified as a % of total listeners)
#NOTE: Variable name "la(x)" = Listener gender group(x):
    #(x=1) = Listeners under 18;
    #(x=2) = Listeners between 18 and 22;   
    #(x=3) = Listeners between 23 and 27;
    #(x=4) = Listeners between 28 and 34;
    #(x=5) = Listeners between 35 and 60;

#[Demog.] Listeners under 18
# (as a % of total listeners);
tl['la1'] = tl['listeners'].astype('int32')
tl['la1'] = (tl['listeners'] 
                  * 0.16).astype('int32')           #Listeners under 18= ~16%;

#[Demog.] Listeners between 18 and 22
# (as a % of total listeners);
tl['la2'] = tl['listeners'].astype('int32')
tl['la2'] = (tl['listeners'] 
                   * 0.36).astype('int32') #Listeners between 18 and 22= ~36%;

#[Demog.] Listeners between 23 and 27
# (as a % of total listeners);
tl['la3'] = tl['listeners'].astype('int32')
tl['la3'] = (tl['listeners'] 
                   * 0.19).astype('int32') #Listeners between 23 and 27= ~19%;

#[Demog.] Listeners between 28 and 34
# (as a % of total listeners);
tl['la4'] = tl['listeners'].astype('int32')
tl['la4'] = (tl['listeners']
                   * 0.17).astype('int32') #Listeners between 28 and 34= ~17%;

#[Demog.] Listeners between 35 and 60
# (as a % of total listeners);
tl['la5'] = tl['listeners'].astype('int32')
tl['la5'] = (tl['listeners'] 
                   * 0.12).astype('int32') #Listeners between 18 and 22= ~12%;

#Rounding the above derived values to whole numbers;
round(tl.la1, 0)
round(tl.la2, 0)
round(tl.la3, 0)
round(tl.la4, 0)
round(tl.la5, 0)

#Printing new 'tl' dataset including demog. values;
print(tl)

#Exporting new 'tl' (generated above) printed output into the orginal Excel file;
writer_obj = pd.ExcelWriter('TIMELINES04162020THRU05172021.xlsx',
                            engine='xlsxwriter')

tl.to_excel(writer_obj, sheet_name='w Demog.s')

writer_obj.save()
print('\n Please check out the TIMELINES04162020THRU05172021.xlsx file. :) \n ')

#Configuring time-series plot for the following(In order):
    #Total listeners;

#Plot: Total Spotify listeners;
fig, ax = plt.subplots()
ax.plot(tl['date'],tl['listeners'])           #Calling 'date', 'listeners' 
ax.set_title('Tone Sinatra: '
             'Total Spotify Listeners 04/16/2020- 05/17/2021')  #Title
ax.set_xlabel('Date')                                                   #Label
ax.set_ylabel('Listeners')                                              #Label
plt.subplots_adjust(hspace=0.3)                                #Adjust spacing
fig.tight_layout(pad=1.0)                                        #Tight layout
plt.show()                                                           #Generate
fig, ax = plt.subplots()


#Configuring time-series plot for the following(In order):
    #Non-Binary identifying listeners;
    #Female identifying listeners; 
    #Male identifying listeners;

#Plot: Non-Binary identifying listeners;
ax.plot(tl['date'],tl['lg3'])                          #Calling 'date', 'nlg3' 
ax.set_title('Tone Sinatra: '
             'Non-Binary identifying '
             'Spotify Listeners ')                                      #Title
ax.set_xlabel('Date')                                                   #Label
ax.set_ylabel('Listeners')                                              #Label
plt.subplots_adjust(hspace=0.3)                                #Adjust spacing
fig.tight_layout(pad=1.0)                                        #Tight layout
plt.show()                                                           #Generate

#Plot: Female identifying listeners;
fig, ax = plt.subplots()
ax.plot(tl['date'],tl['lg2'])                           #Calling 'date', 'lg2' 
ax.set_title('Tone Sinatra: '
             'Female identifying '
             'Spotify Listeners ')                                      #Title
ax.set_xlabel('Date')                                                   #Label
ax.set_ylabel('Listeners')                                              #Label
plt.subplots_adjust(hspace=0.3)                                #Adjust spacing
fig.tight_layout(pad=1.0)                                        #Tight layout
plt.show()                                                           #Generate

#Plot: Male identifying listeners;
fig, ax = plt.subplots()
ax.plot(tl['date'],tl['lg1'])                           #Calling 'date', 'la1' 
ax.set_title('Tone Sinatra: '
             'Male identifying '
             'Spotify Listeners ')                                      #Title
ax.set_xlabel('Date')                                                   #Label
ax.set_ylabel('Listeners')                                              #Label
plt.subplots_adjust(hspace=0.3)                                #Adjust spacing
fig.tight_layout(pad=1.0)                                        #Tight layout
plt.show()                                                           #Generate



#Configuring time-series plot for the following(In order):
    #Listeners under 18;
    #Listeners between 18 and 22;   
    #Listeners between 23 and 27;
    #Listeners between 28 and 34;
    #Listeners between 35 and 60;
    
#Plot: Listeners under 18;
fig, ax = plt.subplots()
ax.plot(tl['date'],tl['la1'])                           #Calling 'date', 'la1' 
ax.set_title('Tone Sinatra: '
             'Spotify Listeners,'
             'Age 18 or under')                                         #Title
ax.set_xlabel('Date')                                                   #Label
ax.set_ylabel('Listeners')                                              #Label
plt.subplots_adjust(hspace=0.3)                                #Adjust spacing
fig.tight_layout(pad=1.0)                                        #Tight layout
plt.show()                                                           #Generate

#Plot: Listeners between 18 and 22;
fig, ax = plt.subplots()
ax.plot(tl['date'],tl['la2'])                           #Calling 'date', 'la2' 
ax.set_title('Tone Sinatra: '
             'Spotify Listeners,'
             'Ages 18-22')                                              #Title
ax.set_xlabel('Date')                                                   #Label
ax.set_ylabel('Listeners')                                              #Label
plt.subplots_adjust(hspace=0.3)                                #Adjust spacing
fig.tight_layout(pad=1.0)                                        #Tight layout
plt.show()                                                           #Generate

#Plot: Listeners between 23 and 27;
fig, ax = plt.subplots()
ax.plot(tl['date'],tl['la3'])                           #Calling 'date', 'la3' 
ax.set_title('Tone Sinatra: '
             'Spotify Listeners,'
             'Ages 23-27')                                              #Title
ax.set_xlabel('Date')                                                   #Label
ax.set_ylabel('Listeners')                                              #Label
plt.subplots_adjust(hspace=0.3)                                #Adjust spacing
fig.tight_layout(pad=1.0)                                        #Tight layout
plt.show()                                                           #Generate

#Plot: Listeners between 28 and 34;
fig, ax = plt.subplots()
ax.plot(tl['date'],tl['la4'])                           #Calling 'date', 'la4' 
ax.set_title('Tone Sinatra: '
             'Spotify Listeners,'
             'Ages 28-34')                                              #Title
ax.set_xlabel('Date')                                                   #Label
ax.set_ylabel('Listeners')                                              #Label
plt.subplots_adjust(hspace=0.3)                                #Adjust spacing
fig.tight_layout(pad=1.0)                                        #Tight layout
plt.show()                                                           #Generate

#Plot: Listeners between 35 and 60;
fig, ax = plt.subplots()
ax.plot(tl['date'],tl['la5'])                           #Calling 'date', 'la5' 
ax.set_title('Tone Sinatra: '
             'Spotify Listeners,'
             'Ages 35-60')                                              #Title
ax.set_xlabel('Date')                                                   #Label
ax.set_ylabel('Listeners')                                              #Label
plt.subplots_adjust(hspace=0.3)                                #Adjust spacing
fig.tight_layout(pad=1.0)                                        #Tight layout
plt.show()                                                           #Generate

























