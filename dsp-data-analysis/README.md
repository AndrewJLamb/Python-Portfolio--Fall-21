#Spotify Exploratory Data Analysis Examples:
#   Objective was to gain better understanding of the demographic makeup of client's audience, using the raw data output from the client's 'Spotify for Artists (SfA)' page. 
#   While possible to collect time-series data on metrics such as Streams, Followers, and Listeners, that is as granular as the export of SfA data gets. 
#   SfA does however provide pie, bar charts showing the approximate demographic makeup of the artist's audience (Given by Spotify users when they create an account).
#     NOTE: The charts for 'Total Listeners Worldwide' are located under the SfA page's 'Audience' tab.
#   Taking into account that exporting the demographic data itself would not be an option, it was clear that one way to gain (rough) insight on this still existed.
#   So, mutiplying the listener demographic percentages (Which are given by SfA, but not included in the export options), by the total listeners data (Which is available to export), would allow for the generation of rough audience demographic data. 
#   Next, the demographic information provided by the SfA 'Audience' tab that was determined to be of interest was broken into two sections: 
#     Section 1: Age-    Which included: Under 18; Ages 18-22; Ages 23-27; Ages 28-34; Ages 35-44; Ages 44-59; And Ages 60+
#     Section 2: Gender- Which included: Male, Female, Non-Binary, and Unspecified categories.
#   The code generated here allowed for the client and their manager to gain much clearer and explicit insight as to what the demographic makeup of their audience really looks like.
#   Information on their audience's demographic makeup has been of great importance when going into meetings with marketing agencies or record labels.