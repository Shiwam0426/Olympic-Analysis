import pandas as pd
import numpy as np

def overTheYears(df,col):
    x=df.drop_duplicates(subset=['Year',col])['Year'].value_counts().reset_index().sort_values(by='Year')
    return x

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[['Name','count','Sport','NOC']]
    x.drop_duplicates(subset=['Name'], inplace=True)
    return x