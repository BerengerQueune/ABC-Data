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


# def main():

#     st.title("TEST")
#     menu = ["Home", "Search", "About"]

#     choice = st.sidebar.selectbox("Menu", menu)

#     df = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_base.csv?token=AU6BUZR7RH7QL3XQCYCQ2P3BS53T4')



#     if choice == 'Home':
#         st.subheader("Home")

#         # with st.expander("Title"):
#         #     mytext = st.text_area("Type Here")
#         #     st.write(mytext)
#         #     st.success("Hello")

#         #st.dataframe(df)
#         movies_title_list = df["primaryTitle"].tolist()

#         movie_choice = st.selectbox("Movie Title", movies_title_list)
#         with st.expander('Movies DF'):
#             st.dataframe(df.head(10))

#             # Filter
#             # img_link = df[df["primaryTitle"] == movie_choice]["img_link"].values[0]
#             # title_link = df[df["primaryTitle"] == movie_choice]["primaryTitle"].values
#             genre = df[df["primaryTitle"] == movie_choice]["Comedy"].values

#         #Layout
#         # st.write(img_link)
#         # st.image(img_link)
#         c1 = st.columns(1)

#         # with c1:
#         #     with st.expander("primaryTitle"):
#         #         st.write(genre)

#         with c1:
#             st.write("lol")
    

    



#     elif choice == "Search":
#         st.subheader("Search By Year")


#     else:
#         st.subheader("About")

# main()

country = ["USA", "India", "Canada", "UK", "Australia"]
st.selectbox("Country", country)

col1, col2  = st.columns(2)

with col1:
	fname = st.text_input("Enter your first name")

with col2:
	lname = st.text_input("Enter your Last name")


st.text_area("Enter your Address")

city, state, zc = st.columns([4,3,2])

with city:
	c = st.text_input("City")

with state:
	s = st.text_input("State")

with zc:
	z = st.text_input("ZipCode")


mail, pn = st.columns([3,1])

with mail:
	email = st.text_input("Enter your Email")

with pn:
	phone = st.text_input("Enter your Phone Number")


#st.button("Save")
if st.button("Save"):
	st.success("Your Information was saved successfully!!")


