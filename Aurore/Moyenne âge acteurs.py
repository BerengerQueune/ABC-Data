#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import ipywidgets as widgets
import datetime as dt
import plotly.express as px


# In[2]:


name_DF = pd.read_csv("name_basics.tsv", sep = "\t", low_memory = False)


# In[3]:


basics_DF = pd.read_csv("title_basics.tsv", sep = "\t", low_memory = False)


# In[4]:


principals_DF = pd.read_csv("title_principals.tsv", sep = "\t", low_memory = False)


# # SELECTIONS DES COLONNES UTILES

# In[5]:


name_DF.drop('deathYear', axis = 1, inplace = True)
name_DF.drop('knownForTitles', axis = 1, inplace = True) 


# In[6]:


basics_DF.drop('primaryTitle', axis = 1, inplace = True)
basics_DF.drop('isAdult', axis = 1, inplace = True)
basics_DF.drop('endYear', axis = 1, inplace = True)


# In[7]:


principals_DF.drop('job', axis = 1, inplace = True)
principals_DF.drop('characters', axis = 1, inplace = True)


# # NETTOYAGE ET FILTRES

# In[8]:


# Nettoyage de la base relative aux acteurs
name_clean_nan = name_DF.dropna(subset = ['primaryProfession'])
name_clean_nan = name_clean_nan[name_clean_nan['primaryProfession'].str.contains('actor|actress')]
name_clean = name_clean_nan[name_clean_nan['birthYear'] != '\\N']

# --> nous avons maintenant un DF contenant uniquement des acteurs et actrices, et dont la colonne 'birthYear' est renseignée


# In[9]:


# Nettoyage de la base relative aux films et films tv :
basics_DF = basics_DF[basics_DF['titleType'].str.contains('movie|tvMovie')]
basics_DF_clean1 = basics_DF[basics_DF['runtimeMinutes'] != '\\N']
basics_DF_clean2 = basics_DF_clean1.astype({"runtimeMinutes": int})
basics_DF_clean = basics_DF_clean2[basics_DF_clean2['runtimeMinutes'] >= 60]
basics_DF_clean = basics_DF_clean.dropna(subset = ['startYear'])
basics_DF_clean = basics_DF_clean[basics_DF_clean['startYear'] != '\\N']
basics_DF_clean = basics_DF_clean.astype({"startYear": int})
basics_DF_clean = basics_DF_clean[basics_DF_clean['startYear'] >= 1894 ]

# --> nous avons maintenant un DF contenant uniquement des films et des films tv dont la durée est supérieure à 60 minutes et dont nous avons des 'startYear' renseignés


# In[10]:


# Nettoyage de la base relative category, contenant les clés des 2 tables précédentes :
principals_DF = principals_DF[principals_DF['category'].str.contains('actor|actress')]

# --> nous pouvons maintenant joindre les 2 bases de données grâce à cette table commune


# # MERGE DES DF

# In[11]:


# Merge principals_DF avec name_clean :

Act_DF = pd.merge(name_clean,principals_DF, how = 'left', left_on=['nconst'], right_on=['nconst'])


# In[12]:


# Merge Act_DF avec basics_DF_clean :

Age_DF = pd.merge(Act_DF,basics_DF_clean, how = 'right', left_on=['tconst'], right_on=['tconst'])
Age_DF.reset_index(inplace = True)


# In[13]:


Age_DF.isna().sum()


# In[14]:


# On remarque que des films n'ont pas d'acteurs à mettre en face. 
# Nous allons donc supprimer ces lignes qui n'ont pas lieu d'être :
Age_DF = Age_DF.dropna(subset = ['nconst'])


# In[15]:


Age_DF.isna().sum()


# In[16]:


Age_DF.isin(['\\N']).sum(axis = 0)


# In[17]:


# Notre base est dorénavant propre.
# Nous allons donc ajouter 1 colonne : celle de l'âge de l'acteur au moment de la 'startYear' :
# Mais avant nous devons transformer les 2 colonnes souhaitées en int :
Age_DF = Age_DF.astype({"startYear": int,"birthYear": int })
Age_DF['Age'] = Age_DF['startYear'] - Age_DF['birthYear']


# In[18]:


Age_DF['Age'].unique()


# In[19]:


# Malgré notre nettoyage des bases de données, nous rencontrons des outliers liés à des fautes de frappe ou autre
# Nous allons donc nettoyer la base pour enlever les outliers (la valeur la + haute sera 110 car à notre connaissance, l'actrice la plus âgée ayant tourné avait 104 ans)

Age_DF_clean_out = Age_DF[Age_DF['Age'] <= 110]
Age_DF_clean = Age_DF_clean_out[Age_DF_clean_out['Age'] >= 0]


# In[20]:


Age_DF_clean.reset_index(inplace = True)


# In[22]:


# Notre DF est prêt mais nous allons ajouter une colonne période pour présenter nos données :
#Age_DF_clean['periode'] = (Age_DF_clean['startYear'] //10) *10


# In[23]:


Age_DF_clean


# # STATS

# In[24]:


# Moyenne âge acteurs de films :
# Calcul de la moyenne d'âge avec .mean() + utilisation de round() pour arrondir le résultat : 

Age_Moyen = round(Age_DF_clean['Age'].mean())
print("La moyenne d'âge des acteurs de films est de", Age_Moyen, "ans au moment du tournage.")


# In[68]:


sns.displot(Age_DF_clean['Age'], kde=True)


# In[51]:


fig, axes = plt.subplots(figsize=(30, 20))

sns.set_style("whitegrid")
boxplot = sns.boxplot(data=Age_DF_clean,  y="Age",
                        showmeans=True, meanprops={"marker": "+", "markeredgecolor": "black", "markersize": "20"})


boxplot.axes.set_title('Age des acteurs et actrices : Zoom',fontsize=50)
boxplot.set_xlabel("Sexe", size = 30)
boxplot.set_ylabel('Age', size = 30)
boxplot.tick_params(labelsize = 20)

moyenne = round(Age_DF_clean['Age'].mean())

plt.show()


# In[56]:


print(" Age des acteurs et actrices : Statistiques :")
print(' ')
print("L'âge moyen des acteurs, tout sexe confondu, est de", moyenne, "ans.")


# In[43]:


fig, axes = plt.subplots(figsize=(30, 20))

sns.set_style("whitegrid")
boxplot = sns.boxplot(data=Age_DF_clean,  x="category", y="Age",
                        showmeans=True, meanprops={"marker": "+", "markeredgecolor": "black", "markersize": "20"})


boxplot.axes.set_title('Age des acteurs et actrices : Zoom',fontsize=50)
boxplot.set_xlabel("Sexe", size = 30)
boxplot.set_ylabel('Age', size = 30)
boxplot.tick_params(labelsize = 20)

plt.show()


# In[40]:


stats_Mean_ages_pivot = ((Age_DF_clean.pivot_table(values='Age', index='category', aggfunc='mean')).round()).astype(int)
stats_Median_ages_pivot = Age_DF_clean.pivot_table(values='Age', index='category', aggfunc='median')
print(" Age des acteurs et actrices : Statistiques :")
print(' ')
print("Voici les moyennes d'âge par sexe : \n", stats_Mean_ages_pivot)
print(' ')
print("Voici l'âge central des populations sexe :\n", stats_Median_ages_pivot)


# In[25]:


fig, axes = plt.subplots(figsize=(30, 20))

sns.set_style("whitegrid")
boxplot = sns.boxplot(data=Age_DF_clean,  x="category", y="Age", hue = 'titleType',
                        showmeans=True, meanprops={"marker": "+", "markeredgecolor": "black", "markersize": "20"})


boxplot.axes.set_title('Age des acteurs et actrices : Zoom',fontsize=50)
boxplot.set_xlabel("Sexe", size = 30)
boxplot.set_ylabel('Age', size = 30)
boxplot.tick_params(labelsize = 20)
boxplot.legend(loc = 'upper right', prop={'size': 30}, borderaxespad=0.)

plt.show()


# In[28]:


stats_Mean_ages_pivot = ((Age_DF_clean.pivot_table(values='Age', index='category', columns='titleType', aggfunc='mean')).round()).astype(int)
stats_Median_ages_pivot = Age_DF_clean.pivot_table(values='Age', index='category', columns='titleType', aggfunc='median')
print(" Age des acteurs et actrices : Statistiques :")
print(' ')
print("Voici les moyennes d'âge par sexe et par catégorie de film: \n", stats_Mean_ages_pivot)
print(' ')
print("Voici l'âge central des populations sexe et par catégorie de film:\n", stats_Median_ages_pivot)


# In[ ]:




