import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from sklearn.neighbors import NearestNeighbors
from gazpacho import get, Soup
import os
import imdb
import imdb.helpers

hide_menu= """
<style>
    #MainMenu {visibility:hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
"""




df_recommandation = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_recommandation.csv?token=AU6BUZU75XQAMO3ALFRQGCTBTZFHU')
df = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/table_finale_alphabetique.csv?token=AU6BUZSDMXLDQHPFUG2YRNLBTZWY4')

st.set_page_config(page_title="ABCS", page_icon=":heart:", layout='wide')

st.markdown("<h1 style='text-align: center; font-family:cursive; color: white;'>Projet recommandation de films de l'équipe ABCS</h1>", unsafe_allow_html=True)

def main():
    def lol():
        st.write("LOOOOL")
    st.button(on_click=lol())


    menu = ["Système de recommandation", "Meaningful KPI"]

    choice = st.sidebar.selectbox("", menu) 

    if choice == 'Système de recommandation':
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write("")
        with c2:
            st.markdown(hide_menu, unsafe_allow_html=True)
        with c3:
            st.write("")

        X = df_recommandation[['Action',
            'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',
            'Drama', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
            'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'Western']]

        st.write("---------------------------------------------------------")





        def url_clean(url):
            base, ext = os.path.splitext(url)
            i = url.count('@')
            s2 = url.split('@')[0]
            url = s2 + '@' * i + ext
            return url


        COUNTRIES = df['primaryTitle'].unique()
        COUNTRIES_SELECTED = st.multiselect('Choisissez vos films préférés :', COUNTRIES)

        # Mask to filter dataframe
        mask_countries = df['primaryTitle'].isin(COUNTRIES_SELECTED)

        data = df[mask_countries]

        user_choice6 = data[['Action',
            'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',
            'Drama', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
            'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'Western']]


        distanceKNN = NearestNeighbors(n_neighbors=5).fit(X)
        mewtwo = user_choice6/len(data)

        mewtwo = mewtwo.sum()
        mewtwo = pd.DataFrame(mewtwo)
        mewtwo = mewtwo.T


        mewtwo = distanceKNN.kneighbors(mewtwo)



        mewtwo = mewtwo[1].reshape(1,5)[0]

        liste_finale = df_recommandation.iloc[mewtwo]


        numero_colonne = 0

        st.write("---------------------------------------------------------")

        # creating instance of IMDb
        ia = imdb.IMDb()

        if len(user_choice6) == 0:
            st.write("Vous n'avez pas encore choisi de film.")
        else:


            cols = st.columns(5)
            for i in range(len(liste_finale)):
                
                
                with cols[numero_colonne]:
                    movie_name = liste_finale.iloc[i]["primaryTitle"]
                    # id
                    code = liste_finale.iloc[i]["tconst"]
                    code = code.replace("tt", "")
                    # # getting information
                    series = ia.get_movie(code)
                    try:
                        # # print the cover
                        st.image(imdb.helpers.fullSizeCoverURL(series), use_column_width='auto', caption=movie_name)
                    except:
                        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYEBKhlYYZa4Saksn04meXChE44J1PU9BCZA&usqp=CAU", 
                        use_column_width="always", caption=movie_name)
                numero_colonne +=1

        # def picture(index):
        #     page = urllib.request.urlopen('https://www.imdb.com/title/' +
        #                                 index.iloc[0, 0] +
        #                                 '/?ref_=adv_li_i%27')
        #     htmlCode = page.read().decode('UTF-8')
        #     soup = Soup(htmlCode)
        #     tds = soup.find("div", {"class": "poster"})
        #     img = tds[0].find("img")
        #     return img.attrs['src']
        
        # picture("tt1392190")
  
        
        
        

    

        
    



    elif choice == "Meaningful KPI":
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

        st.title("Projet : recommandations de films")  # add a title

        st.write("Ce projet effectué au sein de l'école Wild Code School a pour but de nous faire créer un moteur de recommandations de films.")

        st.write("Un cinéma en perte de vitesse situé dans la Creuse vous contacte. Il a décidé de passer le cap du digital en créant un site Internet taillé pour les locaux.")

        st.write("Pour commencer, nous devons explorer la base de données afin de répondre aux questions suivantes :")
        st.write("- Quels sont les pays qui produisent le plus de films ?")
        st.write("- Quels sont les acteurs les plus présents ? À quelle période ?")
        st.write("- La durée moyenne des films s’allonge ou se raccourcit avec les années ?")
        st.write("- Les acteurs de série sont-ils les mêmes qu’au cinéma ?")
        st.write("- Les acteurs ont en moyenne quel âge ?")
        st.write("- Quels sont les films les mieux notés ? Partagent-ils des caractéristiques communes ?")


        fig = px.bar(presence_acteur, x="primaryName", y ='index', color = 'index',
            title = 'Quels sont les acteurs les plus présents ?',
            labels = {'primaryName': 'Nombre de films', 'index': 'Acteurs'},
            width=800, height=600)

        fig.update_layout(showlegend=False, title_x=0.5, yaxis={'visible': True}, template='plotly_dark')

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
        fig.update_layout(template='plotly_dark')
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

        fig.update_layout(showlegend=False, title_x=0.5)

        st.plotly_chart(fig)

        test5 = px.bar(top10, x='Pays', y='Nb de films', color="Nb de films", color_continuous_scale=px.colors.sequential.Viridis, title = 'Pays produisants le plus de film depuis 1960', width=700, height=500, template='plotly_dark')

        st.plotly_chart(test5)



        ######################
        fig = make_subplots(rows=2, cols=2)

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),
                    row=1, col=1)

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),
                    row=1, col=2)

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),
                    row=2, col=1)

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),
                    row=2, col=2)

        fig.update_xaxes(title_text="", row=1, col=1)
        fig.update_yaxes(title_text="", row=1, col=1)

        fig.update_xaxes(title_text="", row=1, col=2)
        fig.update_yaxes(title_text="", row=1, col=2, range=[80, 100])

        fig.update_xaxes(title_text="", row=1, col=1)
        fig.update_yaxes(title_text="", row=2, col=1, range=[50, 100])

        fig.update_xaxes(title_text="", row=1, col=2)
        fig.update_yaxes(title_text="", row=2, col=2, range=[0, 100])

        fig.update_layout(height=1000, width=1400, title_text="Evolution de la durée des films en minutes depuis 1960", title_x=0.5, showlegend=False, template='plotly_dark', autosize=False)

        st.plotly_chart(fig)
        ######################



        fig = px.bar(data_frame = concat_liste_50, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["darkred", "green"],labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films"))
        fig.update_layout(title_text="Top 20 des acteurs ayant tournés autant au cinéma qu'à la TV", width=1000, height=600, template='plotly_dark')

        st.plotly_chart(fig)



        fig = px.bar(data_frame = concat_listeTopFilm, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["blue", "lime"], labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films", color = 'type'))
        fig.update_layout(title_text="Top 20 des acteurs ayant tournés le plus du film au cinéma", title_x=0.5, width=1000, height=600, template='plotly_dark')

        st.plotly_chart(fig)


        fig = px.bar(data_frame = concat_listeTopTV, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["orange", "olive"], labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films"))
        fig.update_layout(title_text="Top 20 des acteurs ayant tournés le plus du film à la télévision", title_x=0.5, width=1000, height=600, template='plotly_dark')

        st.plotly_chart(fig)







main()




# def picture(index):
#     page = urllib.request.urlopen('https://www.imdb.com/title/' +
#                                   index.iloc[0, 0] +
#                                   '/?ref_=adv_li_i%27')
#     htmlCode = page.read().decode('UTF-8')
#     soup = Soup(htmlCode)
#     tds = soup.find("div", {"class": "poster"})
#     img = tds[0].find("img")
#     return img.attrs['src']
# st.subheader(f'_Parce que vous appreciez {movie_selected}_')
#             cols = st.beta_columns(4)
#             for i, col in enumerate(cols):
#                 index_mov = ml_db[ml_db.index == reco.iloc[0, i+1]][['tconst', 'Titre']]
#                 col.subheader(index_mov.iloc[0, 1])
#                 col.image(picture(index_mov))