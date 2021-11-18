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


# CSS code to hide footer and header automatically installed on streamlit page
# I keep the main menu so people can switch from dark to light and vice versa
hide_menu= """
<style>
    #MainMenu {visibility:visible;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
"""



# Loading dataframe, df_input_movies = movie your choose
# df_output_movies = movie suggested
df_output_movies = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_recommandation.csv?token=AU6BUZU75XQAMO3ALFRQGCTBTZFHU')
df_input_movies = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/table_finale_alphabetique.csv?token=AU6BUZSDMXLDQHPFUG2YRNLBTZWY4')


#set the page layout to automatically use full horoizontal size + get and icon and name inside the internet browser
st.set_page_config(page_title="ABCS", page_icon=":heart:", layout='wide')



# Def main contains everything on the page
def main():
    # This is used to activate the CSS code at the top
    st.markdown(hide_menu, unsafe_allow_html=True)
    
    
    # Menu and Sidebar creation
    menu = ["Système de recommandation", "Meaningful KPI"]
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

        genres_divided_by_number_of_movies = user_choice6/len(data)
        sum_of_genres = genres_divided_by_number_of_movies.sum()
        df_sum_of_genres = pd.DataFrame(sum_of_genres)
        df_final_genres = df_sum_of_genres.T


        df_final_genres = distanceKNN.kneighbors(df_final_genres)

        df_final_genres = df_final_genres[1].reshape(1,5)[0]

        liste_finale = df_output_movies.iloc[df_final_genres]


        numero_colonne = 0

        #st.write("---------------------------------------------------------")
        st.write(" ")
        st.write(" ")

        # creating instance of IMDb
        ia = imdb.IMDb()

        if len(user_choice6) == 0:
            pass
        else:

            st.markdown("<h5 style='text-align: center;'>Ces films devraient plaire à vos clients :</h5>", unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
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


main()


