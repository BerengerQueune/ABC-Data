import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import datetime as dt
import plotly.express as px
import ipywidgets as widgets
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from sklearn.neighbors import NearestNeighbors


df_recommandation = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_recommendation.csv?token=AU6BUZUA5UESEPKRRJQIESLBS53UU')
df = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_base.csv?token=AU6BUZWHN456IAMFBUWFFSDBTELCU')

#st.set_page_config( layout='wide')


def main():

    st.title("TEST")
    menu = ["Home", "Search", "About"]

    choice = st.sidebar.selectbox("Menu", menu) 


    if choice == 'Home':
        st.subheader("Home")

        # with st.expander("Title"):
        #     mytext = st.text_area("Type Here")
        #     st.write(mytext)
        #     st.success("Hello")

        #st.dataframe(df)
        movies_title_list = df["primaryTitle"].tolist()

        movie_choice = st.selectbox("Movie Title", movies_title_list)
        # with st.expander('Movies DF'):
        #     st.dataframe(df.head(10))

            # Filter
            # img_link = df[df["primaryTitle"] == movie_choice]["img_link"].values[0]
            # title_link = df[df["primaryTitle"] == movie_choice]["primaryTitle"].values
            # genre = df[df["primaryTitle"] == movie_choice]["Comedy"].values
        genre = df[df["primaryTitle"] == movie_choice]["primaryTitle"].tolist()

        #Layout
        # st.write(img_link)
        # st.image(img_link)
        col1, col2 = st.columns(2)

        # with c1:
        #     with st.expander("primaryTitle"):
        #         st.write(genre)

        with col1:
            with st.expander("primaryTitle"):              
                st.write(genre)

        with col2:
	        lname = st.text_input("Enter your Last name")
    

    



    elif choice == "Search":
        st.subheader("Search By Year")


    else:
        st.subheader("About")






main()

user_choice = ['Kate & Leopold']

col1, col2 = st.columns(2)

with col1:
    user_choice = st.text_input("Enter the name of your favorite movie in the list")

with col2:
    user_choice = st.text_input("Enter the name of your favorite movie in the list")
	        


user_choice2 = df[df['primaryTitle'].isin(user_choice)]

user_choice3 = user_choice2[['Action',
       'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',
       'Drama', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
       'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'Western']]

X = df_recommandation[['Action',
       'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',
       'Drama', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
       'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'Western']]

distanceKNN = NearestNeighbors(n_neighbors=1).fit(X)

mewtwo = distanceKNN.kneighbors(user_choice3)

mewtwo = mewtwo[1].reshape(1,1)[0]
liste_finale = df_recommandation.iloc[mewtwo]

for i in range(len(user_choice)):
  liste_base = user_choice[i]
  newlist = liste_finale["primaryTitle"].iloc[i]
  print (f"En remplacement du film {liste_base} je propose {newlist}.")


liste_finale