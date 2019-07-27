
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[2]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[9]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 
          'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 
          'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 
          'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 
          'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 
          'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 
          'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 
          'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 
          'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 

          'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[14]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:
    
    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    import re
    data = []
    search_string = "edit"
    raw_string = r"[\[]" + r"\b" + search_string + r"\b" + r"[\]]"
    sep = '('
    statename = ""
    with open("university_towns.txt", "r") as file:
        for line in file:
            if re.search(raw_string, line):
                statename = re.sub(raw_string, '', line).rstrip("\n")
            else: 
                regionName = line.split(sep, 1)[0].rstrip()
                data.append([statename, regionName])
    
        towns_df = pd.DataFrame(data, columns = ['State', 'RegionName'])                       
        #print(towns_df.shape)
        #print(towns_df.head())
    return towns_df

#print(get_list_of_university_towns())
#"ANSWER"


# In[29]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    gdpxls = pd.read_excel('gdplev.xls', skiprows = 219)
    #print(gdpxls.columns)
    gdpxls = gdpxls.drop(gdpxls.columns[[0, 1, 2, 3, 7]], axis = 1)
    gdpxls.columns = ['Quarter', 'GDP', 'GDP2009']
    #print(gdpxls.head())
    #print(gdpxls['GDP'][0])
    #print(gdpxls['GDP'][1])
    #print(gdpxls['GDP'][2])
    #print(gdpxls['Quarter'][0])
    for i in range(2, len(gdpxls)):
        if (gdpxls['GDP'][i-2] > gdpxls['GDP'][i-1]) and (gdpxls['GDP'][i - 1] > gdpxls['GDP'][i]):
            return gdpxls['Quarter'][i-2]
    ##return 
#get_recession_start()
#"ANSWER"


# In[31]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    gdpxls = pd.read_excel('gdplev.xls', skiprows = 219)
    #print(gdpxls.columns)
    gdpxls = gdpxls.drop(gdpxls.columns[[0, 1, 2, 3, 7]], axis = 1)
    gdpxls.columns = ['Quarter', 'GDP', 'GDP2009']
    start_year = get_recession_start()
    idx = gdpxls[gdpxls['Quarter'] == start_year].index[0]
    for i in range(idx+3, len(gdpxls)):
        if (gdpxls['GDP'][i-2] < gdpxls['GDP'][i-1]) and (gdpxls['GDP'][i-1] < gdpxls['GDP'][i]):
            return gdpxls['Quarter'][i]
        
# get_recession_end()
#    return 
#"ANSWER"


# In[32]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    gdpxls = pd.read_excel('gdplev.xls', skiprows = 219)
    #print(gdpxls.columns)
    gdpxls = gdpxls.drop(gdpxls.columns[[0, 1, 2, 3, 7]], axis = 1)
    gdpxls.columns = ['Quarter', 'GDP', 'GDP2009']
    start_year = get_recession_start()
    start_idx = gdpxls[gdpxls['Quarter'] == start_year].index[0]
    end_year = get_recession_end()
    end_idx = gdpxls[gdpxls['Quarter'] == end_year].index[0]
    #print(start_idx)
    #print(end_idx)
    gdp = gdpxls[start_idx: end_idx + 1]
    ans = gdp['GDP'].min()
    #print(ans)
    bottom_idx = gdpxls[gdpxls['GDP'] == ans].index[0]
    return gdpxls['Quarter'][bottom_idx]
    #return "ANSWER"
#get_recession_bottom()


# In[20]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df = pd.read_csv('City_Zhvi_AllHomes.csv')
    #print(hdata.columns[[0]+list(range(3,51))])
    df = df.drop(df.columns[[0]+list(range(3,51))],axis=1)
    quarters_df = pd.DataFrame(df[['State','RegionName']])
    #print(quarters_df.head())
    for year in range(2000, 2016):
        quarters_df[str(year) + 'q1'] = df[[str(year) + '-01', str(year) + '-02', str(year) + '-03']].mean(axis = 1)
        quarters_df[str(year) + 'q2'] = df[[str(year) + '-04', str(year) + '-05', str(year) + '-06']].mean(axis = 1)
        quarters_df[str(year) + 'q3'] = df[[str(year) + '-07', str(year) + '-08', str(year) + '-09']].mean(axis = 1)
        quarters_df[str(year) + 'q4'] = df[[str(year) + '-10', str(year) + '-11', str(year) + '-12']].mean(axis = 1)
    year = 2016
    quarters_df[str(year) + 'q1'] = df[[str(year) + '-01', str(year) + '-02', str(year) + '-03']].mean(axis = 1)
    quarters_df[str(year) + 'q2'] = df[[str(year) + '-04', str(year) + '-05', str(year) + '-06']].mean(axis = 1)
    quarters_df[str(year) + 'q3'] = df[[str(year) + '-07', str(year) + '-08']].mean(axis = 1)
    quarters_df.replace({"State": states}, inplace = True)
    quarters_df.set_index(['State', 'RegionName'], inplace = True)
    #print(quarters_df.head())
    #print(quarters_df.shape)
    #df = pd.DataFrame(index_col = ["State", "RegionName"])
    #df = pd.read_csv("City_Zhvi_AllHomes.csv", index_col = ["State", "RegionName"])
    #df = df.loc[:, '2000-01':]
    #df['2000q1'] = df[['2000-01', '2000-02', '2000-03']].mean(axis = 1).rename('2000q1') #.rename('2000q1')
    #print(hdata.columns)
    #print(new_col)
    #df[['2006', '2007']].mean(axis = 1).rename('avgGDP')
    #print(tuple(df.columns).split())
    #print(df.drop(columns = [df.columns[:4].split()], axis = 1))
    #print(df.head())
    return quarters_df
#convert_housing_data_to_quarters().loc["Texas"].loc["Austin"].loc["2010q3"]
#convert_housing_data_to_quarters()
#"ANSWER"


# In[33]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    data = convert_housing_data_to_quarters().copy()
    data = data.loc[:,'2008q3':'2009q2']
    data = data.reset_index()
    def price_ratio(row):
        return (row['2008q3'] - row['2009q2'])/row['2008q3']
    
    data['up&down'] = data.apply(price_ratio,axis=1)
    #uni data 
    
    uni_town = get_list_of_university_towns()['RegionName']
    uni_town = set(uni_town)

    def is_uni_town(row):
        #check if the town is a university towns or not.
        if row['RegionName'] in uni_town:
            return 1
        else:
            return 0
    data['is_uni'] = data.apply(is_uni_town,axis=1)
    
    
    not_uni = data[data['is_uni']==0].loc[:,'up&down'].dropna()
    is_uni  = data[data['is_uni']==1].loc[:,'up&down'].dropna()
    def better():
        if not_uni.mean() < is_uni.mean():
            return 'non-university town'
        else:
            return 'university town'
    p_val = list(ttest_ind(not_uni, is_uni))[1]
    result = (True,p_val,better())
    return result
#run_ttest()
    #return "ANSWER"


# In[ ]:




