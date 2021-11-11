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




test1 = px.line(film, x='startYear', y = 'runtimeMinutes', title = 'Evolution de la durée des films depuis 1960', labels=dict(startYear="Année", runtimeMinutes="Durée en minutes"), 
        width=600, height=400, color_discrete_sequence = ['red'])

st.plotly_chart(test1)


test2 = px.line(film, x='startYear', y = 'runtimeMinutes', title = 'Evolution de la durée des films depuis 1960', labels=dict(startYear="Année", runtimeMinutes="Durée en minutes"), 
        width=600, height=400, range_y=(80,100), color_discrete_sequence = ['green'])

st.plotly_chart(test2)

test3 = px.line(film, x='startYear', y = 'runtimeMinutes', title = 'Evolution de la durée des films depuis 1960', labels=dict(startYear="Année", runtimeMinutes="Durée en minutes"), 
        width=600, height=400, range_y=(50,100), color_discrete_sequence = ['blue'])

st.plotly_chart(test3)

test4 = px.line(film, x='startYear', y = 'runtimeMinutes', title = 'Evolution de la durée des films depuis 1960', labels=dict(startYear="Année", runtimeMinutes="Durée en minutes"), 
        width=600, height=400, range_y=(0,100), color_discrete_sequence = ['orange'])

st.plotly_chart(test4)

fig = px.bar(data_frame = concat_liste_50, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["darkred", "green"],labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films"))
fig.update_layout(title_text="Top 20 des acteurs ayant tournés autant au cinéma qu'à la TV", width=1000, height=600)

st.plotly_chart(fig)



fig = px.bar(data_frame = concat_listeTopFilm, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["blue", "lime"], labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films", color = 'type'))
fig.update_layout(title_text="Top 20 des acteurs ayant tournés le plus du film au cinéma", title_x=0.5, width=1000, height=600)

st.plotly_chart(fig)


fig = px.bar(data_frame = concat_listeTopTV, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["orange", "olive"], labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films"))
fig.update_layout(title_text="Top 20 des acteurs ayant tournés le plus du film à la télévision", title_x=0.5, width=1000, height=600)

st.plotly_chart(fig)