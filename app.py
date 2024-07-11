import streamlit as st 
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from medal_tally import medal_tally, country_year_list, fetch_medal_tally
from preprocess import preprocessing
from OverallAnalysis import overTheYears,most_successful
from countryWiseAnalysis import countryWise,sport,top_10_athelete
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.io as pio

df = pd.read_csv('athlete_events.csv')
df = preprocessing(df)
st.sidebar.title('Olympic Analysis')
st.sidebar.image("https://i.pinimg.com/originals/27/07/eb/2707ebe3f9114547b13a6ad01daf5f51.png")
with st.sidebar:
    user_menu = st.radio(
        "Select an option",
        ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete-wise Analysis")
    )

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = country_year_list(df)
    selected_year = st.sidebar.selectbox('Select year', years)
    selected_country = st.sidebar.selectbox('Select country', country)
    
    if selected_country == "Overall" and selected_year == "Overall":
        st.title("Overall Performances in Olympics")
    elif selected_country != "Overall" and selected_year == "Overall":
        st.title("Overall Performance of " + str(selected_country))
    elif selected_country == "Overall" and selected_year != "Overall":
        st.title("Overall Performance in " + str(selected_year))
    elif selected_country != "Overall" and selected_year != "Overall":
        st.title(str(selected_country) + " Performance in " + str(selected_year))
    
    medal_tally = fetch_medal_tally(df, selected_year, selected_country)
    st.table(medal_tally)

if user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['NOC'].unique().shape[0]
    
    st.title("Statistical Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    team_participated_over_time = overTheYears(df, 'NOC')
    fig = px.line(team_participated_over_time, x='Year', y="count")
    st.title("Participated Teams over the Years")
    st.plotly_chart(fig)
    
    event_over_time = overTheYears(df, 'Event')
    fig = px.line(event_over_time, x='Year', y="count")
    st.title("Events over the Years")
    st.plotly_chart(fig)
    
    athletes_over_time = overTheYears(df, 'Name')
    fig = px.line(athletes_over_time, x='Year', y="count")
    st.title("Athletes over the Years")
    st.plotly_chart(fig)
    
    sport_over_time = overTheYears(df, 'Sport')
    fig = px.line(sport_over_time, x='Year', y="count")
    st.title("Sports over the Years")
    st.plotly_chart(fig)

    st.title("Number of Events over the Years (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(subset=['Year', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int8'), annot=True)
    st.pyplot(fig)

    st.title("Most successful olympics players")

    sport_list=df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select an sport',sport_list)

    st.table(most_successful(df,selected_sport))

if user_menu=="Country-wise Analysis":
    st.title("Country Wise Medal tally")
    country=df["NOC"].unique().tolist()
    country.sort()
    selected_country=st.selectbox('select a country',country)

    temp_df=countryWise(selected_country)
    fig=px.line(temp_df,x='Year',y='Total')
    st.plotly_chart(fig)

    st.title("MedalTally Analysis (Every sport)")
    

    x=sport(selected_country)
    fig,ax= plt.subplots(figsize=(20, 20))
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Total').fillna(0).astype('int8'),annot=True)
    st.pyplot(fig)

    st.title("Top-10 Athletes of "+selected_country)
    x=top_10_athelete(selected_country)
    x=x.sort_values(by='Total',ascending=False)
    st.table(x)

if user_menu=="Athlete-wise Analysis":
    st.title('Winning probablity according to age')
    athlete_df=df.drop_duplicates(subset=['Name','NOC'])
    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Distribution','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    st.plotly_chart(fig)