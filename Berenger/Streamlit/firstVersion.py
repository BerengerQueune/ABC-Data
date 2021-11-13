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


df_recommandation = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_recommendation.csv?token=AU6BUZUA5UESEPKRRJQIESLBS53UU')


#st.set_page_config( layout='wide')


def main():

    st.title("TEST")
    menu = ["Home", "Search", "About"]

    choice = st.sidebar.selectbox("Menu", menu)

    df = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_base.csv?token=AU6BUZR7RH7QL3XQCYCQ2P3BS53T4')



    if choice == 'Home':
        st.subheader("Home")

        # with st.expander("Title"):
        #     mytext = st.text_area("Type Here")
        #     st.write(mytext)
        #     st.success("Hello")

        st.dataframe(df)
        movies_title_list = df["primaryTitle"].tolist()

        movie_choice = st.selectbox("Movie Title", movies_title_list)
    
    
    
    
    
    elif choice == "Search":
        st.subheader("Search By Year")


    else:
        st.subheader("About")

main()


