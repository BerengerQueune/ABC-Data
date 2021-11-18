import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import imdb
import imdb.helpers


# CSS code to hide footer and header automatically installed on streamlit page
# I keep the main menu so people can switch from dark to light and vice versa
hide_menu= """
<style>
    #MainMenu {visibility:visible;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
"""



# Loading dataframe, df_input_movies = your favorite movies
# df_output_movies = movie suggested
df_output_movies = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_recommandation.csv?token=AU6BUZU75XQAMO3ALFRQGCTBTZFHU')
df_input_movies = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/table_finale_alphabetique_numero_2.csv?token=AU6BUZVXK46AQSMDSIAFPITBT6KLG')


#set the page layout to automatically use full horoizontal size + get and icon and name inside the internet browser
st.set_page_config(page_title="ABCS", page_icon=":heart:", layout='wide')



# Def main contains everything on the page
def main():
    # This is used to activate the CSS code at the top
    st.markdown(hide_menu, unsafe_allow_html=True)
    
    
    # Menu and Sidebar creation
    menu = ["Système de recommandation", "Meaningful KPI", "Présentation du Projet"]
    choice = st.sidebar.selectbox("", menu) 

    # Result from your choice inside the menu
    if choice == 'Système de recommandation':

        # CSS code withing markdown to center the title
        st.markdown("<h1 style='text-align: center;'>Recommandation de films</h1>", unsafe_allow_html=True)

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

    if choice == 'Présentation du Projet':
        st.title("Présentation du Projet")
        st.subheader('')
        st.subheader("Le Projet")

        st.markdown(
        """
        Le _PROJET ABC'S_ est issu d’un projet d’école organisé par la __Wild Code School__. Il intervient dans le cadre de notre formation de Data Analyst, 2 mois après son début.
        L’objectif de ce projet est le suivant :
        Nous sommes une équipe de Data Analysts freelance.
        Un cinéma en perte de vitesse situé dans la Creuse nous contacte car il a décidé de passer le cap du digital en créant un site Internet taillé pour les locaux.
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
        """
        )
        st.write("Tous les quatre formons l'équipe ABC'S Data.")
        col1, col2, col3 = st.columns(3)
        with col2:
            st.image("https://d1qg2exw9ypjcp.cloudfront.net/assets/prod/24134/210x210-9_cropped_1377120495_p182hcd8rofaq1t491u06kih16o13.png")

        st.subheader('')
        st.subheader("Notre cliente")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://i.ibb.co/0hnKBMX/Framboise2.png")

        st.markdown(
        """
        Notre cliente est Framboise de Papincourt, petite fille du Comte de Montmirail. Elle a 25 ans et dirige un cinéma en perte de vitesse qui s'appelle "LE KINO".
        Elle fait appel à nous car elle est désespérée. Son cinéma ne fait pas de bénéfice, ses créanciers sont à sa porte et ses problèmes financiers sont tels qu'elle a dû demander un nouveau prêt dans une banque alors que c'est contre ses principes.
        Issue d'une famille noble, elle ne peut pas faire non plus appel à ses proches qui sont fortunés, car elle a renié sa famille. En effet ses derniers ne partagent pas sa vision des choses; exemple : elle est vegan alors que l'activité principale de sa famille est la chasse...
        Elle diffusait initialement des films qui la touchaient afin d'essayer de partager sa vision du monde. Ainsi, les films diffusés étaient principalement des documentaires traitant de l'écologie, du féminisme et de la paix universelle.
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
            *Films : types, durées...
        """
        )
        st.markdown(
        """ 
            *Acteurs : nombre de films, type de films...
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
	        *Recommandation de films proches d’un film cible grâce à un modèle de **KNN**
        """
        )
        st.markdown(
        """ 
	        *Proposition d’une rétrospective avec un modèle de **Régression Logistique**
        """
        )

        st.subheader('')
        st.subheader("Outils")

        st.markdown(
        """
        Le projet est entièrement fait sous **Python** avec une touche de CSS.
        Nous avons utilisé les librairies suivantes :    
        - Pandas
        - Sklearn
        - Plotly
        - Streamlit
        - IMDbPY
        """
        )

        st.subheader('')
        st.subheader("Base de données")

        st.markdown(
        """
        Comme énoncé ci-avant, notre client nous a fourni une base de données basée sur la plateforme IMDb. 
        Nous pouvons les retrouver [**ici**](https://datasets.imdbws.com/), l'explicatif des datasets [**là**](https://www.imdb.com/interfaces/).
        Nous laissons à disposition notre analyse de ces bases de données sur Github dans notre espace collaboratif [**fichier colab**](https://COLLAB)
        """
        )

main()


