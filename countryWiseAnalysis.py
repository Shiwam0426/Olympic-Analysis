import numpy as np
import pandas as pd

df=pd.read_csv('athlete_events.csv')
df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)

def countryWise(selected_country):
    x=df[df['NOC']==selected_country]
    x=x.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values(by='Year',ascending=True).reset_index()
    x['Total']=x['Gold']+x['Silver']+x['Bronze']
    return x

def sport(selected_country):
    temp_df=df[df['NOC']==selected_country]
    x=temp_df.groupby(['Sport','Year']).sum()[['Gold','Silver','Bronze']].sort_values(by='Sport',ascending=True).reset_index()
    x['Total']=x['Gold']+x['Silver']+x['Bronze']
    return x

def top_10_athelete(selected_country):
    temp_df=df[df['NOC']==selected_country]
    x=temp_df.groupby(['Name']).sum()[['Gold','Silver','Bronze']].sort_values(by='Gold',ascending=False).reset_index().head(10)
    x['Total']=x['Gold']+x['Silver']+x['Bronze']
    return x