import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk


import datetime as dt
import plotly.express as px
import ipywidgets as widgets

df = pd.read_csv("https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/B%C3%A9renger/Database_projet/table_finale.csv?token=AU6BUZTSDWGQT72TG2OURMTBSZVT4")  # read a CSV file inside the 'data" folder next to 'app.py'
# df = pd.read_excel(...)  # will work for Excel files

st.title("Hello world!")  # add a title
st.write(df)  # visualize my dataframe in the Streamlit app

acteur_par_periode = pd.read_csv("https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/B%C3%A9renger/Database_projet/acteur_par_periode.csv?token=AU6BUZT4SLQ5IMKG7ZXG673BRZWZS")


fig = px.bar(acteur_par_periode, x = 'count', y="rank", text ='primaryName', color = 'primaryName',
    title = 'Quels sont les acteurs les plus présents par périodes ?',
    labels = {'startYear': 'Période', 'primaryName': 'Acteurs'},
    orientation='h',
    animation_frame="startYear",
    range_x=[0,150],
    range_y=[0,6],
    width=800, height=500)
 
fig.update_traces(textfont_size=12, textposition='outside')
fig.update_layout()
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

fig.update_layout(showlegend=False, title_x=0.5)

st.plotly_chart(fig)