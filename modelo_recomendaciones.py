import pandas as pd
from sklearn.cluster import KMeans
import pickle

# Cargar los datos de películas y calificaciones
movie_data = pd.read_excel("dimMovie.xlsx")
movie_data.columns = ['movieId', 'title', 'gender', 'releaseDate', 'ParticipantName',
                      'Roleparticipant', 'AwardMovie']

watchs_data = pd.read_csv("FactWatch.csv", sep=";", usecols=["idUser", "movieId", "rating"])

# Fusionar los datos
movies_data = watchs_data.merge(movie_data, on="movieId", how="left")

# Crear tabla pivote con las calificaciones por género
tabla_model = pd.pivot_table(movies_data, values='rating', index=['idUser'],
                             columns=['gender'], aggfunc="mean").reset_index()

# Entrenar el modelo KMeans
kmeans_1 = KMeans(n_clusters=5, random_state=0)
kmeans_1.fit(tabla_model[['Action', 'Adventure', 'Animation', 'Children', 'Comedy',
                          'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                          'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 
                          'Western']].fillna(0))

# Guardar el modelo entrenado en un archivo pickle
with open('kmeans_model.pkl', 'wb') as file:
    pickle.dump(kmeans_1, file)

print("Modelo KMeans entrenado y guardado en 'kmeans_model.pkl'")
