######################################################################################
######################################################################################
###########################     LIBRAIRIES    ########################################
######################################################################################
######################################################################################

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
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import imdb
import imdb.helpers


######################################################################################
######################################################################################
###########################     CSS CODE   ###########################################
######################################################################################
######################################################################################

# CSS code to hide footer and header automatically installed on streamlit page
# I keep the main menu so people can switch from dark to light and vice versa
hide_menu= """
<style>
    #MainMenu {visibility:visible;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
"""

######################################################################################
######################################################################################
###########################     DONNEES    ###########################################
######################################################################################
######################################################################################

#df_recommandation = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_recommendation.csv?token=AU6BUZUA5UESEPKRRJQIESLBS53UU')
df = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_base.csv?token=AU6BUZWHN456IAMFBUWFFSDBTELCU')
FULL_DF = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/DF_FULL_GENRES211117.csv?token=AUTGRH2WPDMVJ7DBATL3KWDBTYLIM')


# Loading dataframe, df_input_movies = your favorite movies
# df_output_movies = movie suggested
df_output_movies = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_recommandation.csv?token=AU6BUZU75XQAMO3ALFRQGCTBTZFHU')
df_input_movies = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/table_finale_alphabetique_numero_2.csv?token=AU6BUZVXK46AQSMDSIAFPITBT6KLG')


######################################################################################
######################################################################################
###########################     FONCTIONS    #########################################
######################################################################################
######################################################################################


@st.cache
def load_df(url):
    df = pd.read_csv(url)
    df.set_index(df.iloc[:,0], inplace=True)
    df = df.iloc[:, 1:]
    return df



######################################################################################
######################################################################################
###########################     INTERFACE    #########################################
######################################################################################
######################################################################################


#set the page layout to automatically use full horoizontal size + get and icon and name inside the internet browser
st.set_page_config(page_title="ABC'S", page_icon=":heart:", layout='wide')


def main():
    # This is used to activate the CSS code at the top
    st.markdown(hide_menu, unsafe_allow_html=True)
    
    
    # Menu and Sidebar creation
    menu = ["Présentation du Projet", "Analyses et KPI","Système de recommandation", "Axes d'Amélioration"]
    choice = st.sidebar.selectbox("", menu) 

    # Result from your choice inside the menu
    if choice == 'Système de recommandation':

        # CSS code within markdown to center the title
        st.markdown("<h1 style='text-align: center;'>Recommandation de Films</h1>", unsafe_allow_html=True)

        # Variable X used for Machine Learning
        X = df_output_movies[['Action',
            'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',
            'Drama', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
            'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'Western']]

        # This create a nice grey line between the title and the multiselect menu
        st.write("---------------------------------------------------------")
        





        # Variables to insert df_input inside the multiselect menu
        MOVIES = df_input_movies['primaryTitle'].unique()
        MOVIES_SELECTED = st.multiselect(' ', MOVIES)

        # Mask to filter dataframe
        mask_movies = df_input_movies['primaryTitle'].isin(MOVIES_SELECTED)
        data = df_input_movies[mask_movies]

        # Variables to gather the genre of all movies selected within the multiselect menu
        user_choice6 = data[['Action',
            'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',
            'Drama', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
            'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'Western']]

        # KNN nearest neighbors to find the 5 nearest neighbors
        distanceKNN = NearestNeighbors(n_neighbors=5).fit(X)
        # I divide the genre of all movies based on the number of movies
        genres_divided_by_number_of_movies = user_choice6/len(data)
        # I make the sum of all genres into a new dataframe in order to find a central point for all the movies selected
        sum_of_genres = genres_divided_by_number_of_movies.sum()
        df_sum_of_genres = pd.DataFrame(sum_of_genres)

        # I transpose rows to columns so the dataframe shape matches the expectation for the recommandation
        df_final_genres = df_sum_of_genres.T

        # KNN method to find the nearest neighbors
        df_final_genres = distanceKNN.kneighbors(df_final_genres)
        # A reshape again... not sure if really required
        df_final_genres = df_final_genres[1].reshape(1,5)[0]
        # Looking for index of movies that matches the most
        liste_finale = df_output_movies.iloc[df_final_genres]

        # Creation of a variable used later to each instance of nearest neighbors (5) within a different columns
        numero_colonne = 0

        # Small space
        st.write(" ")
        st.write(" ")

        # creating instance of IMDb this is a library to easily get the poster of the movie recommanded
        ia = imdb.IMDb()
        # if/else: if there is 0 movie selected, then there is no recommandation
        if len(user_choice6) == 0:
            pass
        else:
            # CSS title followed by space
            st.markdown("<h5 style='text-align: center;'>Ces films devraient plaire à vos clients :</h5>", unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            # Creation of 5 columns
            cols = st.columns(5)
            for i in range(len(liste_finale)):
                
                # For Each columns
                with cols[numero_colonne]:
                    # Get the name of the movie
                    movie_name = liste_finale.iloc[i]["primaryTitle"]
                    # Get the tconst (used to gather poster image)
                    code = liste_finale.iloc[i]["tconst"]
                    # Remove the "tt" string at start of the tconst
                    code = code.replace("tt", "")
                    # getting information from the movie related to previous tconst
                    series = ia.get_movie(code)
                    try:
                        # If there is a cover for this movie, print the cover + the name of the movie as caption and use automatically full size of the column
                        st.image(imdb.helpers.fullSizeCoverURL(series), use_column_width='auto', caption=movie_name)
                    except:
                        # If there is no cover, use this image picked randomly over internet + the name of the movie as caption and use automatically full size of the column
                        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYEBKhlYYZa4Saksn04meXChE44J1PU9BCZA&usqp=CAU", 
                        use_column_width="always", caption=movie_name)
                # Add one to the numero_colonne variable so next nearest neighbors will be inside the following column
                numero_colonne +=1



######################################################################################
######################################################################################
###########################     AURORE     ###########################################
######################################################################################
######################################################################################
    if choice == "Présentation du Projet":
                # CSS code within markdown to center the title
        st.markdown("<h1 style='text-align: center;'>Présentation du Projet</h1>", unsafe_allow_html=True)
                # This create a nice grey line between the title and the multiselect menu
        st.write("---------------------------------------------------------")
        st.subheader('')
        st.subheader("Le Projet")

        st.markdown(
        """
        Le _PROJET ABC'S_ est issu d’un projet d’école organisé par la __Wild Code School__. Il intervient dans le cadre de notre formation de Data Analyst, 2 mois après son début.

        L’objectif de ce projet est le suivant :

        Nous sommes une équipe de Data Analysts freelance.
        Un cinéma en perte de vitesse situé dans la Creuse nous contacte ca rl a décidé de passer le cap du digital en créant un site Internet taillé pour les locaux.
        Notre client nous demande de créer un moteur de recommandations de films qui à terme, enverra des notifications via internet.

        Aucun client du cinéma n'ayant à ce jour renseigné ses préférences, nous sommes donc dans une situation de __cold start__. Cependant, notre client nous a fourni une base de données basée sur la plateforme IMDb.

        """
        )
        st.subheader('')
        st.subheader("L'équipe")

        st.markdown(
        """
        Notre équipe est composée de 4 élèves issus de la promo Data Green de la __Wild Code School__ :
        - [Aurore LEMAÎTRE](https://github.com/alema86)
        - [Bérenger QUEUNE](https://github.com/BerengerQueune)
        - [Christophe LEFEBVRE](https://github.com/clefebvre2021)
        - [Stéphane ESSOUMAN](https://github.com/Liostephe)

        Tous les quatre formons l'équipe ABC'S Data.
        """
        )
        col1, col2, col3 = st.columns(3)
        with col2:
            st.image("https://d1qg2exw9ypjcp.cloudfront.net/assets/prod/24134/210x210-9_cropped_1377120495_p182hcd8rofaq1t491u06kih16o13.png")

        st.subheader('')
        st.subheader("Notre client(e)")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://i.ibb.co/0hnKBMX/Framboise2.png")

        st.markdown(
        """
        Notre cliente est Framboise de Papincourt, petite fille du Comte de Montmirail. Elle a 25 ans et dirige un cinéma en perte de vitesse qui s'appelle "LE KINO".

        Elle fait appel à nous car elle est désespérée. Son cinéma ne fait pas de bénéfice, ses créanciers sont à sa porte et ses problèmes financiers sont tels qu'elle a dû demandé un nouveau prêt dans une banque alors que c'est contre ses principes.

        Issue d'une famille de nobles, elle ne peut pas faire non plus appel à ses proches qui sont fortunés, car elle a renié sa famille. En effet ses derniers ne partagent pas sa vision des choses; exemple : elle est vegan alors que l'activité principale de sa famille est la chasse...

        Elle diffusait initialement des films qui la touchaient afin d'essayer de partager sa vision du monde. Ainsi, la films diffusés étaient principalement des documentaires traitant de l'écologie, du féminisme et de la paix universelle.

        Elle est obligée de faire changer de cap son cinéma et est prête à diffuser des films qui vont à l'encontre de ses convictions si ça lui permet de ne pas mettre la clé sous la porte et éviter d'être la raillerie de sa famille.
        Faire du bénéfice à terme serait un plus, car ça lui permettrait d'offrir à ses futurs enfants Harmony, Safran et Kiwi un environnement dans lequel ils pourront s'épanouir comme elle en rêve.

        Ainsi, elle nous donne carte blanche dans le rendu de notre travail.
        """  
        )    
        st.subheader('')
        st.subheader("Notre mission")

        st.markdown(
        """
        Nous devons fournir à notre client les outils d’analyse de la base de données issue de **IMDB**.
       
        Il nous est demandé de :
        """
        )
        st.markdown(
        """ 
        - Faire une rapide présentation de la base de données (sur notre espace collaboratif sur Github)
        """
        )
        st.markdown(
        """ 
        - Fournir à notre client quelques statistiques sur les films :
        """
        )
        st.markdown(
        """ 
            * Films : types, durées...
        """
        )
        st.markdown(
        """ 
            * Acteurs : nombre de films, type de films...
        """
        )
        st.markdown(
        """ 
        - Présenter les TOP 10 des films par années et genre
        """
        )
        st.markdown(
        """ 
        - Présenter les TOP 5 des acteurs/actrices par années et genre
        """
        )
        st.markdown(
        """ 
        - Retourner une liste de films recommandés en fonction d'IDs ou de noms de films choisis par un utilisateur
        """
        )
        st.markdown(
        """ 
        - Il faudra entraîner des outils de Machine Learning : 
        """
        )
        st.markdown(
        """ 
	        * Recommandation de films proches d’un film cible grâce à un modèle de **KNN**
        """
        )
        st.markdown(
        """ 
	        * Proposition d’une rétrospective avec un modèle de **Régression Logistique**
        """
        )

        st.subheader('')
        st.subheader("Outils")

        st.markdown(
        """
        Le projet est entièrement fait sous **Python**.

        Nous avons utilisés entres autres les librairies suivantes :    
        - Pandas
        - Sklearn
        - Plotly
        - Streamlit
        - CSS
        """
        )

        st.subheader('')
        st.subheader("Base de données")

        st.markdown(
        """
        Comme énoncé ci-avant, notre client nous a fourni une base de données basée sur la plateforme IMDb. 
        Nous pouvons les retrouver [**ici**](https://datasets.imdbws.com/), l'explicatif des datasets [**là**](https://www.imdb.com/interfaces/).

        Nous laissons à dispositions notre analyse de ces bases de données sur Github dans notre espace collaboratif [**fichier colab**](https://github.com/BerengerQueune/ABC-Data)
        """
        )

######################################################################################
######################################################################################
###########################     BERENGER     #########################################
######################################################################################
######################################################################################

    if choice == 'Movie recommandation':
        st.subheader("Movie recommandation")
                
######################################################################################
######################################################################################
###########################     AURORE     ###########################################
######################################################################################
######################################################################################   



    elif choice == "Analyses et KPI":

        
        
        
        
        
        link2 = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/film3.csv?token=AU6BUZQSZO7FES64E636CRLBS2IWM'
        film = pd.read_csv(link2)


        


        #######################################
        ########  Introduction     ############
        #######################################

                        # CSS code within markdown to center the title
        st.markdown("<h1 style='text-align: center;'>Analyses et KPI</h1>", unsafe_allow_html=True)
                # This create a nice grey line between the title and the multiselect menu
        st.write("---------------------------------------------------------")
        st.write("")
        st.subheader("Analyses de la base de données et KPI") # add a subtitle

        st.write("Comme énoncé dans notre partie **'Présentation du Projet'**, il nous est demandé de :")
        st.markdown(
        """
        - Faire une rapide présentation de la base de données (que vous pouvez retrouver [ici](https://github.com/BerengerQueune/ABC-Data/blob/main/Aurore/Analyses_BDD_Etape%201.ipynb))
        - Faire une analyse complète de la base de données, en répondant aux questions suivantes :
            * Quels sont les pays qui distribuent le plus de films ?
            * Quels sont les acteurs les plus présents ? À quelle période ?
            * La durée moyenne des films s’allonge ou se raccourcit avec les années ?
            * Les acteurs de série sont-ils les mêmes qu’au cinéma ? 
            * Les acteurs ont en moyenne quel âge ? 
            * Quels sont les films les mieux notés ? Partagent-ils des caractéristiques communes ?
        """
        )
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        #######################################
        ########    GRAPHIQUES     ############
        #######################################

        #######################################
        ########  Q01 -Christophe  ############
        #######################################
        st.subheader("Quels sont les pays qui distribuent le plus de films ?") # add a subtitle


        top10 = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/top10.csv?token=AU6BUZSEQED65VJVLNSX4FLBS2IYO')

        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(' ')
            st.markdown(
                """
                Le dataset a été élaboré à partir de deux fichiers : title.basics et title.akas.

                Lors de notre analyse de la base de données, nous avons pu observer une grande variété de types d'oeuvres répertoriées par IMDb. 

                Ainsi, à partir de title.basics, il a été choisi de ne retenir que les films ('movie') et téléfilms ('tvMovie) réalisés après 1960, limitant notre périmètre d’analyse aux films les plus récents. Les courts-métrages (“short”) ont également été retirés.
                Les lignes n'ayant pas de données pour les items suivants ont été supprimées de notre DataFrame: année de réalisation ('startYear'), de durée ('runtimeMinutes') ou de genres ('genres').

                De la même façon, les films qui n’ont pas de région dans le fichiers title.akas ont été supprimés.

                Une jointure a été réalisée entre les deux DataFrame afin d’ajouter la région aux colonnes de la base de données title.basics.

                Afin de réaliser le graphique, un [dataframe attitré](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/top10.csv?token=AU6BUZSEQED65VJVLNSX4FLBS2IYO) reprenant  le top 10 des pays ayant distribué le plus de films et téléfilms a été produit.

                [Lien Notebook](https://github.com/BerengerQueune/ABC-Data/blob/main/Christophe/Projet%202%20-%20Quels%20sont%20les%20pays%20qui%20produisent%20le%20plus%20de%20films.ipynb)

                """
                )

        with col2:
            top10Graph = px.bar(top10, x='Pays', y='Nb de films', color="Nb de films")
            top10Graph.update_layout(title_text="Palmarès des pays selon la distribution des oeuvres cinématographiques", title_x=0.5, width=1000, height=600, template='plotly_dark')
            st.plotly_chart(top10Graph)

        st.write("")
        st.image("https://i.ibb.co/NV1RFNH/C-mod.png") 
        st.markdown("""
                Ce graphique montre clairement une prédominance des USA dans le nombre de films distribués, puisque leur nombre dépasse la somme de ceux réalisés dans les deux pays suivants à savoir la Grande-Bretagne et la France.               
                A noter que l’on retrouve en troisième position des films dont l’origine est inconnue XWW. Cette région signifie 'World Wide' et correspond aux oeuvres que l'on peut retrouver sur internet (web, Youtube...).
                On note également que trois des 5 continents sont représentés dans le top10.
                La France confirme cependant sa position de cinéphile en étant dans le top 3 si nous excluons la région 'XWW'.
                """
                )
        st.write(' ')
        st.write(' ')
        st.write(' ')
        #####################################
        ########  Q02 -Bérenger  ############
        #####################################
        st.subheader("Quels sont les acteurs les plus présents ?") # add a subtitle
 
        presence_acteur = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/presence_acteurs.csv?token=AU6BUZU76KCNKK6X5NKIZ6DBTZPVI')

        col1, col2 = st.columns([2, 1])
        with col2:
            st.write(' ')
            st.markdown(
                """
                Le dataset a été élaboré à partir de 3 fichiers : name.basics.tsv, title.principals.tsv et title.basics.tsv.

                Nous avons nettoyé la base de données de la façon suivante :
                - dans le df relatif à 'title.principals.tsv', nous avons gardé les colonnes 'tconst', 'titleType', 'startYear', 'runtimeMinutes' et 'genres'
                    - dans la colonne 'category' nous avons gardé les 'actor' et 'actress'
                    - dans la colonne 'character', nous avons supprimé les ```\R```, les 'Narrator', 'Various' et 'Additional Voices'
                - dans le df relatif à 'title.basics.tsv', nous avons gardé les colonnes 'tconst', 'nconst', 'category' et 'characters'
                **EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE**

                Afin de réaliser le graphique, un [dataframe attitré]('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/presence_acteurs.csv?token=AU6BUZU76KCNKK6X5NKIZ6DBTZPVI') reprenant les 20 acteurs les plus présents quelle que soit l'époque a été produit.

                [Lien Notebook](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Quels_sont_les_acteurs_les_plus_pr%C3%A9sents.ipynb?token=AUTGRHYRYCTRXKOZDDLVIELBTZL3I)

                """
                )

        with col1:
            fig = px.bar(presence_acteur, x="primaryName", y ='index', color = 'index',
            title = 'Quels sont les acteurs les plus présents ?',
            labels = {'primaryName': 'Nombre de films', 'index': 'Acteurs'},
            width=800, height=600)

            fig.update_layout(showlegend=False, title_x=0.5, yaxis={'visible': True}, template='plotly_dark')

            st.plotly_chart(fig)

        st.write("")
        st.image("https://i.ibb.co/bHkZJb7/B-mod.png") 
        st.markdown("""
                **EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE**
                """
                )


        st.write(' ')
        st.write(' ')
        st.write(' ')
        #####################################
        ########  Q03 -Bérenger  ############
        #####################################
        st.subheader("Quels sont les acteurs les plus présents, à quelle période ?") # add a subtitle

        acteur_par_periode = pd.read_csv("https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/acteur_par_periode.csv?token=AUTGRH4M4FBOFMK6DAW3X33BT6Z2S")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(' ')
            st.markdown(
                """
                
                **EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE**

                Afin de réaliser le graphique, un [dataframe attitré]('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/acteur_par_periode.csv?token=AU6BUZWYJ6GYLJLQVDQCLZTBSZ2NK') reprenant les 5 acteurs les plus présents pour chaque décennies depuis 1910.

                [Lien Notebook](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Quels_sont_les_acteurs_les_plus_pr%C3%A9sents.ipynb?token=AUTGRHYRYCTRXKOZDDLVIELBTZL3I)

                """
                )

        with col2:
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

        st.write("")
        st.image("https://i.ibb.co/bHkZJb7/B-mod.png") 
        st.markdown("""
                **EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE**
                """
                )
        st.write(' ')
        st.write(' ')
        st.write(' ')
        #######################################
        ########  Q04 -Christophe  ############
        #######################################
        st.subheader("La durée moyenne des films s’allonge ou se raccourcit avec les années ?") # add a subtitle
 
        presence_acteur = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/presence_acteurs.csv?token=AU6BUZU76KCNKK6X5NKIZ6DBTZPVI')

        st.markdown(
                """
                Le dataset a été élaboré à partir d’un seul fichier : title.basics.tsv.

                Le fichier title.basics a été traité comme pour la question relative aux pays les plus distributeurs (Q01), à l’exception du type qui a été limité aux films ('movie'); les 'tvMovie' ont donc été supprimés.
                Nous avons calculé la durée moyenne des films par année et conservé que les années échues.

                Afin de réaliser le graphique, un [dataframe attitré](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/presence_acteurs.csv?token=AU6BUZU76KCNKK6X5NKIZ6DBTZPVI) reprennant toutes les informations requises a été produit.

                [Lien Notebook]('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Christophe/Projet%202%20-%20La%20dur%C3%A9e%20moyenne%20des%20films%20s%E2%80%99allonge%20ou%20se%20raccourcit%20avec%20les%20ann%C3%A9es.ipynb?token=AUTGRH3TRSZ7CDJ62ME6XU3BT44DO')

                """
            )

        fig = make_subplots(rows=2, cols=2)

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),row=1, col=1)
        fig.update_xaxes(title_text="", row=1, col=1)
        fig.update_yaxes(title_text="", row=1, col=1)

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]), row=1, col=2)
        fig.update_xaxes(title_text="", row=1, col=2)
        fig.update_yaxes(title_text="", row=1, col=2, range=[80, 100])

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),row=2, col=1)
        fig.update_xaxes(title_text="", row=1, col=1)
        fig.update_yaxes(title_text="", row=2, col=1, range=[50, 100])

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),row=2, col=2)
        fig.update_xaxes(title_text="", row=1, col=2)
        fig.update_yaxes(title_text="", row=2, col=2, range=[0, 100])

        fig.update_layout(height=1000, width=1400, title_text="Evolution de la durée des films en minutes depuis 1960", title_x=0.5, showlegend=False, template='plotly_dark', autosize=False)

        st.plotly_chart(fig)

        st.write("")
        st.image("https://i.ibb.co/NV1RFNH/C-mod.png") 
        st.markdown("""
                La lecture du premier graphique (en haut à gauche), donne l’impression d’une grande variabilité de la durée des films entre 1960 et 2020.
                Il s’agit en fait d’un biais de lecture lié à l’échelle utilisée. Comme la durée varie réellement peu (entre 87 et 95 mn), l’échelle du graphique a été automatiquement adaptée et fait ressortir une variation importante.
                
                Les trois graphiques suivants montrent donc les données avec une échelle de plus en plus large.

                Si l’on regarde le dernier graphique (avec une échelle de 0 à 100), la durée des films d’une année sur l’autre paraît à peu près stable.
                """
                )
        st.write(' ')
        st.write(' ')
        st.write(' ')
        #######################################
        ########  Q05 -Christophe  ############
        #######################################
        st.subheader("Les acteurs de série sont-ils les mêmes qu’au cinéma ?") # add a subtitle
 
        concat_liste_50 = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_liste50.csv?token=AU6BUZSY6OPPE25EYFUWFELBS2IS4')
        concat_listeTopFilm = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_listeTopFilm.csv?token=AU6BUZUX7HJJXUSIP47YANLBS2IVA')
        concat_listeTopTV = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_listeTopTV.csv?token=AU6BUZWRESNKYQ36Y652SJLBS2IVW')

        st.markdown(
                """
                Le dataset a été élaboré à partir de trois fichiers : title.basics et title.principals et name.basics.

                Le fichier title.basics a été traité comme pour la question n°1.
                
                A partir de title.basics, il a été choisi de ne retenir que les films et téléfilms réalisés à partir de 1960, afin de limiter le périmètre d’analyse aux films les plus récents. Les courts métrages (“short”) ont également été retirés.
                Un certain nombre de ces films n’ont pas d’année de réalisation, de durée ou de genres. Ils ont donc été supprimés de la base.

                Le fichier title.principals a été filtré pour ne conserver que les items actrices et acteurs. Le fichier name.basics à permis de faire le lien avec leur nom.

                Afin de réaliser le graphique, 3 dataframes attitrés reprenant toutes les informations dont nous avions besoin ont été produits :
                - [Top 20 des acteurs ayant tourné autant de films que de téléfilms](concat_liste_50)
                - [Top 20 des acteurs ayant tourné le plus de films](concat_listeTopFilm)
                - [Top 20 des acteurs ayant tourné le plus de téléfilms](concat_listeTopTV)

                [Lien Notebook](https://github.com/BerengerQueune/ABC-Data/blob/main/Christophe/Projet%202%20-%20Quels%20sont%20les%20pays%20qui%20produisent%20le%20plus%20de%20films.ipynb)

                Les éléments en notre possession nous ont permis de créer 3 graphiques :
                """
            )

        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.markdown(
                """
                        **Top 20 des acteurs ayant tourné autant de films que de téléfilms**

                         Il s’agit des acteurs des acteurs qui ont tourné le plus tout en faisant autant de téléfilm que de film.
                        La quantité de films par acteurs semble assez faible par rapport aux deux catégories suivantes.
                """
                )

        with col2:
            fig = px.bar(data_frame = concat_liste_50, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["darkred", "green"],labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films"))
            fig.update_layout(title_text="Top 20 des acteurs ayant tournés autant au cinéma qu'à la TV", width=1000, height=600, template='plotly_dark')

            st.plotly_chart(fig)

        st.write("")
        st.write("")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.markdown(
                """
                        **Top 20 des acteurs ayant tourné le plus de films**

                        Le graphique montre clairement que les acteurs ayant le plus tournés au cinéma ont fait très peu de téléfilms.
                        Il faut effectivement zoomer sur le graphique pour s’apercevoir que 4 d’entre aux ont tournés dans un ou deux téléfilms seulement.
                """
                )

        with col2:
            fig = px.bar(data_frame = concat_listeTopFilm, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["blue", "lime"], labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films", color = 'type'))
            fig.update_layout(title_text="Top 20 des acteurs ayant tournés le plus de films au cinéma", title_x=0.5, width=1000, height=600, template='plotly_dark')

            st.plotly_chart(fig)

        st.write("")
        st.write("")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.markdown(
                """
                        **Top 20 des acteurs ayant tourné le plus de téléfilms**

                        On s’aperçoit qu’à l’inverse des acteurs de cinéma, les acteurs ayant tournés le plus de téléfilms ont également tournés des films au cinéma.
                        Cependant, au global ont remarque qu'ils ont tournés dans moins de films mais ont tous fait au moins des apparitions au cinéma.
                """
            )

        with col2:
            fig = px.bar(data_frame = concat_listeTopTV, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["orange", "olive"], labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films"))
            fig.update_layout(title_text="Top 20 des acteurs ayant tournés le plus de téléfilms", title_x=0.5, width=1000, height=600, template='plotly_dark')

            st.plotly_chart(fig)
        
        st.write('')
        st.write(' ')
        st.write(' ')

        #######################################
        ##########  Q06 -Aurore  ##############
        #######################################
        st.subheader("Les acteurs ont en moyenne quel âge ?") # add a subtitle
        Age_DF_clean = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/Age_acteurs20211118.csv?token=AUTGRH6AOVYKCSBEBIWDCLTBT5VZI')
        st.markdown(
                """
                Le dataset a été élaboré à partir de 3 fichiers : name.basics.tsv, title.principals.tsv et title.basics.tsv.

                Après sélection des colonnes à utiliser, nous avons nettoyé la base de données comme à notre habitude.

                Nous avons appliqué les filtres suivants, tant pour notre analyse que pour des besoins techniques (limite de taille du csv)
                - sélection de tous les acteurs et actrices
                - sélection des films et téléfilms dont la durée est supérieure à 60 minutes et dont la date de production est postérieure à 1960
                
                Après la jointure des 3 dataset, nous avons :
                - ajouté une colonne "âge" qui correspond à la différence entre les valeurs des colonnes 'birthYear' et 'startYear'
                - du fait d'une base pas 'propre', nous avons discriminé les outliers et gardé pour la colonne 'âge' toutes les valeurs situées entre 0 et 110

                Afin de réaliser le graphique, un [dataframe attitré]('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/Age_acteurs20211118.csv?token=AUTGRH6AOVYKCSBEBIWDCLTBT5VZI') reprenant les données dont nous avions besoin pour la présentation des graphiques a été produit.

                [Lien Notebook]('https://github.com/BerengerQueune/ABC-Data/blob/main/Aurore/KPI/Moyenne%20%C3%A2ge%20Acteurs.ipynb')

                """
                )
        st.image("https://i.ibb.co/4SxFQYy/A-mod.png")
        
        
        ######GRAPH01#########
        col1, col2 = st.columns([2, 1])
        with col2:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.markdown(
                """
                D'après ce boxplot, la moyenne d'âge, tout sexe confondu, est de 40 ans.
                **EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE**
                """
                )

        with col1:


            fig = go.Figure()
            fig.add_trace(go.Box(y=Age_DF_clean["Age"], name = 'Population', marker_color='lightgreen', boxmean=True # represent mean
            ))
            fig.update_yaxes(title= 'Age')

            fig.update_layout(title_text="Age des acteurs et actrices : Zoom", title_x=0.5, width=1000, height=600, template='plotly_dark')



            st.plotly_chart(fig)
        st.write("")    
        st.write("")






        ######GRAPH02#########
        col1, col2 = st.columns([2, 1])
        with col2:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ') 
            st.write(' ')
            st.write(' ')
            st.write(' ')            
            st.markdown(
                """
                Voici les moyennes d'âge par genre, pour les personnes ayant tourné dans des films et des téléfilms :
                - Acteurs :     43 ans
                - Actrices :    36 ans

                Voici l'âge central pour ces mêmes populations :
                - Acteurs :     41 ans
                - Actrices :    32 ans

                **EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE**
                """
                )

        with col1:
            fig = go.Figure()
            fig = px.box(Age_DF_clean,y="Age", color="category")
            fig.update_yaxes(title= 'Age')
            fig.update_xaxes(title= 'Population')

            fig.update_layout(title_text="Age des acteurs et actrices : par genre", title_x=0.5, width=1000, height=600, template='plotly_dark')
            
            st.plotly_chart(fig)

        #st.write("")    
        #st.write("")





        ######GRAPH03#########
        col1, col2 = st.columns([2, 1])
        with col2:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ') 
            st.markdown(
                """
                Voici les moyennes d'âge par sexe et par catégorie de film :
                - Films :
                    - Acteurs :     42 ans
                    - Actrices :    35 ans
                - Téléfilms :
                    - Acteurs :     45 ans
                    - Actrices :    40 ans
                            
 
                Voici l'âge central des populations sexe et par catégorie de film :
                - Films :
                    - Acteurs :     41 ans
                    - Actrices :    31 ans
                - Téléfilms :
                    - Acteurs :     44 ans
                    - Actrices :    37 ans

                **EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE**
                """
                )

        with col1:
            fig = go.Figure()
            fig = px.box(Age_DF_clean, x="titleType", y="Age", color="category")
            fig.update_yaxes(title= 'Age')

            fig.update_layout(title_text="Age des acteurs et actrices : par type de film et genre", title_x=0.5, width=1000, height=600, template='plotly_dark')
            

            st.plotly_chart(fig)
        st.write("")

        st.markdown("""
                
                **EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE**
                """
                )

        st.write('')
        st.write(' ')
        st.write(' ')
        #######################################
        ##########  Q07 -Aurore  ##############
        #######################################
        st.subheader("Quels sont les films les mieux notés ?") # add a subtitle


        qualify_movies = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/DF_FULL_GENRES211117.csv?token=AUTGRH2J25FKEQLFK7VPH5TBT7DVE')
        st.write(' ')
        st.markdown(
                """
                Le dataset a été élaboré à partir de 5 fichiers : name_basics.tsv, title_basics.tsv, title_principasl.tsv, title_ratings.csv et title_akas.csv .

                Après sélection des colonnes à utiliser, nous avons nettoyé la base de données comme à notre habitude. 

                Nous avons principalement utilisé les mêmes filtres que pour la question suivante afin de garder une cohérence dans notre analyse, et toujours aussi pour des raisons techniques (Dataset hébergés sur Github).

                Dans ce dataset, nous avons aussi ajouté une colonne 'moyenne_pondérée', qui pondère les valeurs de la colonne 'averageRating' selon celles de la colonne 'numVotes', selon la formule de pondération de la note fournie par IMDb :

                st.latex(r```
                    Weighted\; Rating (WR) = (\frac{v}{v + m} . R) + (\frac{m}{v + m} . C)
                    ```)

                Où :
                - v est le nombre de votes (= numVotes)
                - m est le nombre minimum de votes requis pour être listé
                - R est la moyenne des notes ditribuées par les votants (= averageRating) 
                - C est le vote moyen sur l'ensemble du dataset

                Nous avons établi une fonction qui est la suivante pour cela :

                code = '''def movie_ponderation(x,m=m,C=C):
                            v=x['numVotes']
                            R=x['averageRating']
                            # calculation based on IMDB formula
    
                            return (v/(v+m)*R) + (m/(m+v)*C)'''
                st.code(code, language='python')
            

                Afin de réaliser le graphique, un [dataframe attitré](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/DF_FULL_GENRES211117.csv?token=AUTGRH2J25FKEQLFK7VPH5TBT7DVE) reprenant toutes les informations dont nous avions besoin pour cette analyse a été produit.

                [Lien Notebook](https://github.com/BerengerQueune/ABC-Data/blob/main/Christophe/Projet%202%20-%20Quels%20sont%20les%20pays%20qui%20produisent%20le%20plus%20de%20films.ipynb)

                """
                )
        st.image("https://i.ibb.co/4SxFQYy/A-mod.png")

        ##################
        st.title('Quels sont les films les mieux notés ?')
        qualify_movies_DF_FULL2 = qualify_movies.sort_values('moyenne_ponderee', ascending=False)
        qualify_movies_DF_FULL2['text_graph'] = 'Note : ' + qualify_movies_DF_FULL2['moyenne_ponderee'].round(2).astype(str) + ', nombre de votes : '+ qualify_movies_DF_FULL2['numVotes'].astype(str)

        fig = px.bar(qualify_movies_DF_FULL2, x='moyenne_ponderee', y='primaryTitle',title = 'Top 10 des films distribués en France depuis 1960', text = 'text_graph', orientation='h', range_x=[0,11],labels = {'moyenne_ponderee': 'Note', 'primaryTitle': 'Films'})
        fig.update_yaxes(range=(9.5, -.5))
        fig.update_layout(title_text="Top 10 des films distribués en France depuis 1960", title_x=0.5, width=1000, height=600, template='plotly_dark')

        st.plotly_chart(fig)

        ################
        st.title('Top 10 des films distribués en France depuis 1960 par décennies')

        groupedDf = qualify_movies.groupby(['Periode', 'primaryTitle'] ).size()
        df_final  = pd.DataFrame({'inter' : groupedDf.groupby(level='Periode').nlargest(5).reset_index(level=0, drop=True)})
        df_final.reset_index(inplace=True)
        df_final2 = df_final.tail(70)
        df_final2['rank'] = df_final2.groupby('Periode')['inter'].rank(method = 'first')

        fig = px.bar(df_final2, x = 'inter',y ='rank', text = 'primaryTitle',color = 'primaryTitle',
        title = 'Top 10 des films distribués en France depuis 1960 par décennies',
        labels = {'Periode': 'Période', 'primaryTitle': 'Films'},
        orientation='h',
        animation_frame="Periode",
        range_x=[0,11],
        range_y=[0,6],
        width=1000, height=800)
 
        fig.update_traces(textfont_size=12, textposition='outside')
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

        fig.update_layout(showlegend=False, title_x=0.5, width=1000, height=600, template='plotly_dark')
            
        st.plotly_chart(fig)

        st.write("")

        st.title('Quels sont les films les mieux notés - Caractéristiques communes ?')
        FULL_DF = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/DF_FULL_GENRES211117.csv?token=AUTGRH6TVDSC4VN4IF6LDHLBT7FC6')


        fig = px.scatter_3d(FULL_DF,x="genre1",y ='genre2', z= 'genre3', color = 'moyenne_ponderee' )
        fig.update_layout(title_text="Caractéristiques communes des films les mieux notés", title_x=0.5, width=1000, height=600, template='plotly_dark')
            
        st.plotly_chart(fig)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.title('Note moyenne par genre de films')
            moyenne_genre = pd.pivot_table(FULL_DF,values="averageRating",columns="genre1",aggfunc=np.mean)
            moyenne_genre_unstacked = moyenne_genre.unstack().unstack()
            moyenne_genre_unstacked =moyenne_genre_unstacked.sort_values('averageRating')

            Genres = moyenne_genre_unstacked.index
            moyenne = moyenne_genre_unstacked['averageRating']

            fig = px.bar(moyenne_genre_unstacked, x=Genres, y =moyenne, labels = {'averageRating': 'Note moyenne', 'genre1': 'Genres de 1er rang'},color = moyenne_genre_unstacked.index,title = 'Note moyenne par genre de films ',width=600, height=450)
            fig.update_layout(showlegend=False, title_x=0.5, yaxis={'visible': True}, template='plotly_dark')
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig)

        with col2:
            st.title('Nombre moyen de votes par genre')
            nb_moyen_votes = pd.pivot_table(FULL_DF,values="numVotes",columns="genre1",aggfunc=np.mean)
            nb_moyen_votes_unstacked = nb_moyen_votes.unstack().unstack()
            nb_moyen_votes_unstacked = nb_moyen_votes_unstacked.sort_values('numVotes').round()

            genres = nb_moyen_votes_unstacked.index
            nb_votes = nb_moyen_votes_unstacked['numVotes']

            fig = px.bar(nb_moyen_votes_unstacked, x=genres, y =nb_votes, labels = {'numVotes': 'Nombre moyen de votes', 'genre1': 'Genres de 1er rang'}, color = nb_moyen_votes_unstacked.index,title = "Nombre moyen de votes par genre",width=600, height=450)
            fig.update_layout(showlegend=False, title_x=0.5, yaxis={'visible': True}, template='plotly_dark')
            fig.update_xaxes(tickangle=-45)
            
            st.plotly_chart(fig)



        st.markdown("""
                **EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE**
                """
                )
        st.write(' ')
        st.write(' ')
        st.write(' ')















        st.write("")

        st.markdown("""
                **EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE EN ATTENTE**
                """
                )
        st.write(' ')
        st.write(' ')
        st.write(' ')











        st.markdown(
                """
                EN COURS DE CONSTRUCTION            EN COURS DE CONSTRUCTION            EN COURS DE CONSTRUCTION            EN COURS DE CONSTRUCTION            
                             EN COURS DE CONSTRUCTION            EN COURS DE CONSTRUCTION            EN COURS DE CONSTRUCTION            EN COURS DE CONSTRUCTION            
                EN COURS DE CONSTRUCTION            EN COURS DE CONSTRUCTION            EN COURS DE CONSTRUCTION            EN COURS DE CONSTRUCTION            
            

                """
                )
















    
        





main()



