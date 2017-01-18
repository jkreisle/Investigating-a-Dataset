
# coding: utf-8

# # Finding Relationships in Baseball Data

# Question: Can any one statistic predict the overall performance of a baseball team? I will test several performance indicators and base performance off the number of wins in any given season.

# In[2]:

import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import unicodecsv
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('whitegrid')
get_ipython().magic(u'matplotlib inline')


# In[3]:

#import the 'Teams' csv file that includes team statistics for a variety of categories.

teams = pd.read_csv('Teams.csv')


# In[4]:

#the number of games varies wildly over the years. Most years have 162 games in a season.

teams['G'].describe()


# In[5]:

games = np.random.normal(size=100)
sns.distplot(teams['G']);
sns.plt.title('Games Played')


# In[6]:

#if we are comparing a team that played less or more games in a given season to another,
#the performance of one of these teams may benefit or suffer from this difference, so
#I attempt to standardize the data by filtering in only seasons with 162 games.

g_162 = teams[teams['G'] == 162].copy()
g_162 = pd.DataFrame(g_162)
g_162['G'].value_counts()


# In[15]:

runs = np.random.normal(size=100)
sns.distplot(g_162['R']);
sns.plt.title('Runs Scored')


# In[16]:

#I will use runs as the first variable to predict wins, as it seems to be the most logical catalyst to winning games. 

g_162['R'].describe()


# In[17]:

#there doesn't appear to be a very strong correlation here (R= 0.5).

sns.jointplot(x="R", y="W", data=g_162, kind="reg");


# In[18]:

#I add another strong indicator of offensive production, batting average, to the dataset.

g_162['BA'] = (g_162.H/g_162.AB)


# In[19]:

battingaverage = np.random.normal(size=100)
sns.distplot(g_162['BA']);
sns.plt.title('Batting Average')


# In[20]:

g_162['BA'].describe()


# In[21]:

#this relationship seems even weaker (R= 0.4).

sns.jointplot(x="BA", y="W", data=g_162, kind="reg");


# In[22]:

#I decide to add an advanced statistic, slugging percentage, to measure hitting for power.
#slugging takes five individual statistics in consideration.

g_162.rename(columns={'2B': 'TWOB', '3B': 'THREEB'}, inplace=True)
g_162['SLG'] = (g_162.H + 2*g_162.TWOB + 3*g_162.THREEB + 4*g_162.HR)/(g_162.AB)


# In[24]:

slugging = np.random.normal(size=100)
sns.distplot(g_162['SLG']);
sns.plt.title('Slugging Percentage')


# In[25]:

g_162['SLG'].describe()


# In[26]:

#this is the weakest relationship (R= 0.36) of all three offensive statistics. 
#perhaps pitching will predict wins more effectively?

sns.jointplot(x="SLG", y="W", data=g_162, kind="reg");


# In[27]:

era = np.random.normal(size=100)
sns.distplot(g_162['ERA']);
sns.plt.title('Earned Run Average')


# In[28]:

g_162['ERA'].describe()


# In[29]:

#a relatively weak relationship (R= -0.52), yet this is actually the strongest indicator tested.

sns.jointplot(x="ERA", y="W", data=g_162, kind="reg");


# In[30]:

#Here I take the top 10 teams based on number of wins and find the average for each statistic. 
#Then calculated the p-value to illustrate how the performance compares to the average of all teams.

most_wins = g_162['W'].nlargest(10)
most_wins = pd.DataFrame(most_wins)
most_wins = most_wins.join(g_162[['R']])
most_wins = most_wins.join(g_162[['ERA']])
most_wins = most_wins.join(g_162[['BA']])
most_wins = most_wins.join(g_162[['SLG']])

runs_difference = ((most_wins['R'].mean())-(g_162['R'].mean()))/(g_162['R'].std())
print runs_difference
era_difference = ((most_wins['ERA'].mean())-(g_162['ERA'].mean()))/(g_162['ERA'].std())
print era_difference
ba_difference = ((most_wins['BA'].mean())-(g_162['BA'].mean()))/(g_162['BA'].std())
print ba_difference
slg_difference = ((most_wins['SLG'].mean())-(g_162['SLG'].mean()))/(g_162['SLG'].std())
print slg_difference


# # Conclusions

# A shortcoming to this analysis is the withholding of statistics in the data set that could actually be a strong indicator of team performance, but were not analyzed here. In addition, some data is missing that, if analyzed, could have provided insights into predicting baseball teams' success.
# 
# Overall, I think its clear that wins in baseball do not result from one statistic, but many. Offense alone is not enough, defense will not win the game, but rather a team that performs well in every aspect of the game will end up with one more 'W' in their column.

# In[230]:

#code created with the help of Myles at Udacity forums
#https://discussions.udacity.com/t/plotting-largest-values-in-a-dataset/198898/1
#https://discussions.udacity.com/t/help-with-filtering-data-in-baseball-set/197747/1
#and Seaborn website tutorial
#http://seaborn.pydata.org/tutorial.html

