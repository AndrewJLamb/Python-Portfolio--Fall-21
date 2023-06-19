#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 23 14:29:25 2021

@author: andrew7
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import seaborn as sns
from pandas.plotting import register_matplotlib_converters # Handle date-time 
register_matplotlib_converters()                           #conversions between
                                                           #pandas and matplotlib

#Using instagramy Python module to scrape individual post data; 
from instagramy import InstagramUser
from instagramy import InstagramPost
#For more information on the methods utilized from Instagramy:
    #https://pypi.org/project/instagramy/#description



#Instagram login cookie session ID:
session_id = "47683141696%3ApIm5ua5IFbaLeQ%3A10"


###                      EWOP STUDIOS                                      ###
###    WEB-SCRAPING : TONE SINATRA, INSTAGRAM PROFILE                      ###
###           BY: ANDREW LAMB, LAURENCE HICKS                              ###
###    (QUESTIONS OR CONCERNS? Email: andrew@ewopstudios.com)              ###


#Beginning the scrape;
#Instagram Post {shortcodes}
#creating variable names for each individual post:
    #p(xx) = post 1;
    #Beginning with earliest post
    #ie., 'p1' = First post by Instagram user @tonesinatra
    
p1 = InstagramPost("CBmOaM0pl0c", from_cache=True)
p2= InstagramPost("CB9dolcJ7s8", from_cache=True)
p3= InstagramPost("CEc9XUHJWCY", from_cache=True)
p4= InstagramPost("CEs1HIwAVvv", from_cache=True)
p5= InstagramPost("CFn6lQQg_Pb", from_cache=True)
p6= InstagramPost("CF-uGbtJNMf", from_cache=True)
p7= InstagramPost("CGJUJZ9gipa", from_cache=True)
p8= InstagramPost("CGvoI21p3hs", from_cache=True)
p9= InstagramPost("CG8TI7FJriQ", from_cache=True)
p10= InstagramPost("CIWuApYJOAv", from_cache=True)
p11= InstagramPost("CJe9nLogvDm", from_cache=True)
p12= InstagramPost("CK5MKoWg-4a", from_cache=True)
p13= InstagramPost("CLaoAVhgYBz", from_cache=True)
p14= InstagramPost("CL7ooGjp54C", from_cache=True)
p15= InstagramPost("CMAzqkpg3Qo", from_cache=True)
p16= InstagramPost("CMneKglJBoJ", from_cache=True)
p17= InstagramPost("CNQfkbJJC3U", from_cache=True)
p18= InstagramPost("CNTRXGfpZxQ", from_cache=True)
p19= InstagramPost("CNYUboVJjDP", from_cache=True)
p20= InstagramPost("CNdrpRfJVO_", from_cache=True)
p21= InstagramPost("CNlSfZKpuhh", from_cache=True)
p22= InstagramPost("CNs5d7epiwq", from_cache=True)
p23= InstagramPost("CNvJyKpJBuW", from_cache=True)
p24= InstagramPost("CNvqUjEpRRD", from_cache=True)
p25= InstagramPost("CN5vypPJfme", from_cache=True)
p26= InstagramPost("CObgrH7ptKF", from_cache=True)
p27= InstagramPost("CO344N7pepw", from_cache=True)
p28= InstagramPost("CPEd4gLJMdi", from_cache=True)
p29= InstagramPost("CPHKTiOJyas", from_cache=True)



#Creating variable names for Instagram post Upload Dates:
        #t_p(xx) = time(uploaded) for post
        #Starting with earliest post first
        
t_p1 = p1.upload_time
t_p2 = p2.upload_time
t_p3 = p3.upload_time
t_p4 = p4.upload_time
t_p5 = p5.upload_time
t_p6 = p6.upload_time
t_p7 = p7.upload_time
t_p8 = p8.upload_time
t_p9 = p9.upload_time
t_p10 = p10.upload_time
t_p11 = p11.upload_time
t_p12 = p12.upload_time
t_p13 = p13.upload_time
t_p14 = p14.upload_time
t_p15 = p15.upload_time
t_p16 = p16.upload_time
t_p17 = p17.upload_time
t_p18 = p18.upload_time
t_p19 = p19.upload_time
t_p20 = p20.upload_time
t_p21 = p21.upload_time
t_p22 = p22.upload_time
t_p23 = p23.upload_time
t_p24 = p24.upload_time
t_p25 = p25.upload_time
t_p26 = p26.upload_time
t_p27 = p27.upload_time
t_p28 = p28.upload_time
t_p29 = p29.upload_time


#Creating dataFrame for Instagram post Upload Dates:
    #t_p(xx) = time(uploaded) for post(xx)
    #Starting with earliest post first;
#DataFrame: Instagram Upload Times(By post)    
upload_date = pd.DataFrame(
    [[t_p1],
    [t_p2],
    [t_p3],
    [t_p4],
    [t_p5],
    [t_p6],
    [t_p7],
    [t_p8],
    [t_p9],
    [t_p10],
    [t_p11],
    [t_p12],
    [t_p13],
    [t_p14],
    [t_p15],
    [t_p16],
    [t_p17],
    [t_p18],
    [t_p19],
    [t_p20],
    [t_p21],
    [t_p22],
    [t_p23],
    [t_p24],
    [t_p25],
    [t_p26],
    [t_p27],
    [t_p28],
    [t_p29]]
    )
print(upload_date)

#Creating variable names for Instagram Likes:
    #lp(xx) = Number of likes for post (xx)
    #Starting with earliest post first;
    
lp1 = p1.number_of_likes
lp2 = p2.number_of_likes
lp3 = p3.number_of_likes
lp4 = p4.number_of_likes
lp5 = p5.number_of_likes
lp6 = p6.number_of_likes
lp7 = p7.number_of_likes
lp8 = p8.number_of_likes
lp9 = p9.number_of_likes
lp10 = p10.number_of_likes
lp11 = p11.number_of_likes
lp12 = p12.number_of_likes
lp13 = p13.number_of_likes
lp14 = p14.number_of_likes
lp15 = p15.number_of_likes
lp16 = p16.number_of_likes
lp17 = p17.number_of_likes
lp18 = p18.number_of_likes
lp19 = p19.number_of_likes
lp20 = p20.number_of_likes
lp21 = p21.number_of_likes
lp22 = p22.number_of_likes
lp23 = p23.number_of_likes
lp24 = p24.number_of_likes
lp25 = p25.number_of_likes
lp26 = p26.number_of_likes
lp27 = p27.number_of_likes
lp28 = p28.number_of_likes
lp29 = p29.number_of_likes

#DataFrame: Instagram Likes(By post)
likes = pd.DataFrame(
    [[lp1],
     [lp2],
     [lp3],
     [lp4],
     [lp5],
     [lp6],
     [lp7],
     [lp8],
     [lp9],
     [lp10],
     [lp11],
     [lp12],
     [lp13],
     [lp14],
     [lp15],
     [lp16],
     [lp17],
     [lp18],
     [lp19],
     [lp20],
     [lp21],
     [lp22],
     [lp23],
     [lp24],
     [lp25],
     [lp26],
     [lp27],
     [lp28],
     [lp29]]
    )
print(likes)

#Creating variable names for Instagram Comments:
    #cp(xx) = Number of comments for post (xx)
    #Starting with earliest post first;

cp1 = p1.number_of_comments
cp2 = p2.number_of_comments
cp3 = p3.number_of_comments
cp4 = p4.number_of_comments
cp5 = p5.number_of_comments
cp6 = p6.number_of_comments
cp7 = p7.number_of_comments
cp8 = p8.number_of_comments
cp9 = p9.number_of_comments
cp10 = p10.number_of_comments
cp11 = p11.number_of_comments
cp12 = p12.number_of_comments
cp13 = p13.number_of_comments
cp14 = p14.number_of_comments
cp15 = p15.number_of_comments
cp16 = p16.number_of_comments
cp17 = p17.number_of_comments
cp18 = p18.number_of_comments
cp19 = p19.number_of_comments
cp20 = p20.number_of_comments
cp21 = p21.number_of_comments
cp22 = p22.number_of_comments
cp23 = p23.number_of_comments
cp24 = p24.number_of_comments
cp25 = p25.number_of_comments
cp26 = p26.number_of_comments
cp27 = p27.number_of_comments
cp28 = p28.number_of_comments
cp29 = p29.number_of_comments

#DataFrame: Instagram Comments(By post)
comments = pd.DataFrame(
    [[cp1],
    [cp2],
    [cp3],
    [cp4],
    [cp5],
    [cp6],
    [cp7],
    [cp8],
    [cp9],
    [cp10],
    [cp11],
    [cp12],
    [cp13],
    [cp14],
    [cp15],
    [cp16],
    [cp17],
    [cp18],
    [cp19],
    [cp20],
    [cp21],
    [cp22],
    [cp23],
    [cp24],
    [cp25],
    [cp26],
    [cp27],
    [cp28],
    [cp29]],
    )
print(comments)




#Containing 'upload date', 'likes', and 'comments' within
#  it's own DataFrame;
data = [upload_date, likes, comments]
headers = ['Upload Date', 'Likes', 'Comments']
IG_data = pd.concat(data, axis=1, keys=headers)
print(f'IG_data(): \n{IG_data}\n')



#Configuring time-series plot for the following(In order):
    #Instagram posts: Likes per post over time
    #Instagram posts: Comments per post over time 
    
#Time-series plots: Instagram Likes per post over time; 
fig, ax = plt.subplots()
ax.plot(IG_data['Upload Date'],IG_data['Likes'])       #Calling 'date', 'likes' 
ax.set_title('@tonesinatra: '
             'Likes per Instagram Post')                                #Title
ax.set_xlabel('Date')                                                   #Label
ax.set_ylabel('Likes')                                                  #Label
plt.subplots_adjust(hspace=0.3)                                #Adjust spacing
fig.tight_layout(pad=1.0)                                        #Tight layout
plt.show()                                                           #Generate


#Time-series plot: Instagram Comments per post over time;
fig, ax = plt.subplots()
ax.plot(IG_data['Upload Date'],IG_data['Comments']) #Calling 'date', 'comments' 
ax.set_title('@tonesinatra: '
             'Comments per Instagram Post')                             #Title
ax.set_xlabel('Date')                                                   #Label
ax.set_ylabel('Comments')                                               #Label
plt.subplots_adjust(hspace=0.3)                                #Adjust spacing
fig.tight_layout(pad=1.0)                                        #Tight layout
plt.show()                                                           #Generate















