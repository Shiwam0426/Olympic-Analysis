import pandas as pd
import numpy as np
from preprocess import preprocessing

# df=pd.read_csv('athelete_events.csv')
# df=preprocessing(df)

def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','Sex','Games','Year','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values(by='Gold',ascending=False).reset_index()
    medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    return medal_tally

def country_year_list(df):
    year=df['Year'].unique().tolist()
    year.sort()
    year.insert(0,'Overall')

    country=df['NOC'].unique().tolist()
    country.sort()
    country.insert(0,'Overall')
    return year,country

def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','Sex','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year=='Overall' and country=='Overall':
        temp_df=medal_df
    elif year=='Overall' and country!='Overall':
        temp_df=medal_df[medal_df['NOC']==country]
        flag=1
    elif year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
        
    else:
        temp_df=medal_df[(medal_df['Year']==int(year)) & (medal_df['NOC']==country)]
    if (flag==1):
           x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values(by='Year',ascending=True).reset_index()
           x['Total']=x['Gold']+x['Silver']+x['Bronze']
    else:
           x=temp_df.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values(by='Gold',ascending=False).reset_index()
           x['Total']=x['Gold']+x['Silver']+x['Bronze']
    return (x)