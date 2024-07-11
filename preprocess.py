import pandas as pd
import numpy as np

# df=pd.read_csv('athlete_events.py')

def preprocessing(df):
    df=df[df['Season']=='Summer']
    df.drop_duplicates(inplace=True)
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df
