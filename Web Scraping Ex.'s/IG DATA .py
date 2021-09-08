#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 23 14:29:25 2021

@author: andrew7
"""
#Importing pandas, specifically for storing data in individual DataFrames;
#Importing InstagramUser from the 'instagramy' Python module in order to access 
#   the profile of interest;

import pandas as pd
from instagramy import InstagramUser
# Obscuring 'sessionid' for privacy purposes. This is the web browser's current
#   session id that enables the scrape of the profile to take place
#Instagram login cookie session ID:
session_id = "{sessionid}"

#Importing InstagramPost from the 'instagramy' Python module, because the objective
#   was to gain a more granular view of Instragram engagement (ie., more than 
#   just an overall number of likes or comments present on the profile)
#Given the nature of the objective, opted for the InstagramPost module in order to
#   keep track of the number of likes, comments, etc. present for each post that was
#   active on the user's profile at the time.
#Using instagramy Python module to scrape individual post data; 
#For more information on the methods utilized from Instagramy:
    #https://pypi.org/project/instagramy/#description

from instagramy import InstagramPost
###                      EWOP STUDIOS                                      ###
###    WEB-SCRAPING : TONE SINATRA, INSTAGRAM PROFILE                      ###
###           BY: ANDREW LAMB, LAURENCE HICKS                              ###
###    (QUESTIONS OR CONCERNS? Email: andrew@ewopstudios.com)              ###


#Beginning the scrape;
#Instagram Post {shortcodes}
    #p(xx) = post 1;
    #Beginning with earliest post
    #ie., 'p1' = First post by Instagram user @{Client Name omitted}
#'instagramy' module:
#   Defining 'p_' as the variable name for each individual post;
#   Using the URL shortcodes (See: strings in curly brackets below)
#Instagram Post {shortcodes}:
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
#'instagramy' module: Collecting the time at which each post was uploaded; 
#Storing in a DataFrame for easy access/manipulation.
#Upload Time: 
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
#Specifying DataFrame;
df1 = pd.DataFrame(
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
print(df1)


#Creating variable names for Instagram Likes:
    #lp(xx) = Number of likes for post (xx)
    #Starting with earliest post first;
#'instagramy' module: Collecting the number of comments on each post that was 
#   active on client's profile; Storing in a DataFrame for easy access/manipulation.
#Likes:
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


#Creating DataFrame for the number of likes on each Instagram post:
    #lp(xx) = time(uploaded) for post(xx)
    #Starting with earliest post first;
#Specifying DataFrame;
df2 = pd.DataFrame(
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
print(df2)


#Creating variable names for Instagram Comments:
    #cp(xx) = Number of comments for post (xx)
    #Starting with earliest post first;
#'instagramy' module: Collecting the number of comments on each post that was 
#   active on client's profile; Storing in a DataFrame for easy access/manipulation.
#Comments:
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


#Creating DataFrame for the number of comments on each Instagram post:
    #cp(xx) = time(uploaded) for post(xx)
    #Starting with earliest post first;
#Specifying DataFrame;
df3 = pd.DataFrame(
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
print()


#Creating new DataFrame, 'data', to contain the three individual sets of data
#   Containing 'upload date', 'likes', and 'comments' within
#   it's own DataFrame;
data = [df1, df2, df3]

#Specifying headers in order to assign the correct names to the correct data;
headers = ['Upload Date', 'Likes', 'Comments']

#Concatenating DataFrame in order to store the relevant data together
IG_data = pd.concat(data, axis=1, keys=headers)
print(f'IG_data(): \n{IG_data}\n')
