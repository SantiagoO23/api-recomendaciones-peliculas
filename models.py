import pandas as pd
import pickle

# Cargar los datos de películas y calificaciones
movie_data = pd.read_excel("dimMovie.xlsx")
movie_data.columns = ['movieId', 'title', 'gender', 'releaseDate', 'ParticipantName',
                      'Roleparticipant', 'AwardMovie']

# Cargar las calificaciones del archivo FactWatch.csv
watchs_data = pd.read_csv("FactWatch.csv", sep=";", usecols=["idUser", "movieId", "rating"])

# Fusionar las calificaciones con los datos de las películas
movies_data = watchs_data.merge(movie_data, on="movieId", how="left")

# Crear tabla pivote para la matriz de usuarios y géneros de películas
tabla_model = pd.pivot_table(movies_data, values='rating', index=['idUser'],
                             columns=['gender'], aggfunc="mean").reset_index()

# Cargar el modelo KMeans previamente entrenado
with open('kmeans_model.pkl', 'rb') as file:
    kmeans_model = pickle.load(file)

# Predecir los clusters para cada usuario
clusters = kmeans_model.predict(tabla_model[['Action', 'Adventure', 'Animation', 'Children', 'Comedy',
                                             'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                                             'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 
                                             'Western']].fillna(0))

# Agregar la columna de clusters al DataFrame de usuarios
tabla_model['Cluster'] = clusters

# Fusionar los clusters de los usuarios con las calificaciones y datos de películas
movies_datacluster = movies_data.merge(tabla_model[['idUser', 'Cluster']], on='idUser', how='left')

print("Modelo KMeans y datos cargados correctamente")
