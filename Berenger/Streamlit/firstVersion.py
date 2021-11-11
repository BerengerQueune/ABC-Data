import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import datetime as dt
import plotly.express as px
import ipywidgets as widgets

st.title("Hello world!")  # add a title

acteur_par_periode = pd.read_csv("https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/acteur_par_periode.csv?token=AU6BUZWYJ6GYLJLQVDQCLZTBSZ2NK")
link = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/top10.csv?token=AU6BUZSEQED65VJVLNSX4FLBS2IYO'
top10 = pd.read_csv(link)
presence_acteur = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/presence_acteurs.csv?token=AU6BUZRUOZP7577TQEBP5ODBS2IXQ')
link2 = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/film3.csv?token=AU6BUZQSZO7FES64E636CRLBS2IWM'
film = pd.read_csv(link2)
link3 = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_liste50.csv?token=AU6BUZSY6OPPE25EYFUWFELBS2IS4'
link4 = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_listeTopFilm.csv?token=AU6BUZUX7HJJXUSIP47YANLBS2IVA'
link5 = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_listeTopTV.csv?token=AU6BUZWRESNKYQ36Y652SJLBS2IVW'
concat_liste_50 = pd.read_csv(link3)
concat_listeTopFilm = pd.read_csv(link4)
concat_listeTopTV = pd.read_csv(link5)

fig = px.bar(presence_acteur, x="primaryName", y ='index', color = 'index',
    title = 'Quels sont les acteurs les plus présents ?',
    labels = {'primaryName': 'Nombre de films', 'index': 'Acteurs'},
    width=800, height=600)

fig.update_layout(showlegend=False, title_x=0.5, yaxis={'visible': True})

st.plotly_chart(fig)

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