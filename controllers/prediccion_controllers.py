from fastapi import Request, HTTPException
from models import tabla_model, movie_data, kmeans_model, movies_datacluster
from typing import List

# Simulación de base de datos 
predictions_db = []

# Obtener el cluster del usuario a partir de su ID
def get_user_cluster(user_id):
    user_data = tabla_model[tabla_model['idUser'] == user_id][['Action', 'Adventure', 'Animation', 'Children', 
                                                               'Comedy', 'Crime', 'Documentary', 'Drama', 
                                                               'Fantasy', 'Film-Noir', 'Horror', 'Musical', 
                                                               'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 
                                                               'War', 'Western']].fillna(0)
    if user_data.empty:
        return None
    return kmeans_model.predict(user_data)[0]

# GET: Leer predicciones pasadas
def get_predictions(pred_id: int = None):
    if pred_id:
        result = next((pred for pred in predictions_db if pred['id'] == pred_id), None)
        if not result:
            raise HTTPException(status_code=404, detail="Predicción no encontrada")
        return result
    return predictions_db

# POST: Realizar una predicción para el usuario
async def create_prediction(request: Request):
    try:
        data = await request.json()
        user_id = data['idUser']
        user_cluster = get_user_cluster(user_id)
        if user_cluster is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en los datos")

        # Películas que ya vio el usuario
        movies_watched_by_user = movies_datacluster[movies_datacluster["idUser"] == user_id]["title"].tolist()

        # Obtener películas del cluster asignado
        movies_in_cluster = movies_datacluster[movies_datacluster['Cluster'] == user_cluster]

        # Filtrar las películas que el usuario no ha visto
        recommended_movies = movies_in_cluster[~movies_in_cluster['title'].isin(movies_watched_by_user)]

        # Ordenar por 'rating' y devolver las 10 mejores recomendaciones
        recommendations = recommended_movies[['title', 'rating']].sort_values(by='rating', ascending=False).head(10)

        # Guardar la predicción en la "base de datos"
        new_prediction = {
            'id': len(predictions_db) + 1,
            'idUser': user_id,
            'input': data,
            'prediction': recommendations.to_dict(orient='records')
        }

        predictions_db.append(new_prediction)
        return new_prediction

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la predicción: {str(e)}")


# PUT: Actualizar una predicción existente
async def update_prediction(pred_id: int, request: Request):
    try:
        data = await request.json()
        pred_to_update = next((pred for pred in predictions_db if pred['id'] == pred_id), None)
        if not pred_to_update:
            raise HTTPException(status_code=404, detail="Predicción no encontrada")

        pred_to_update['input'] = data
        user_id = data['idUser']
        user_cluster = get_user_cluster(user_id)
        if user_cluster is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en los datos")

        # Películas que ya vio el usuario
        movies_watched_by_user = movies_datacluster[movies_datacluster["idUser"] == user_id]["title"].tolist()

        # Obtener películas del cluster asignado
        movies_in_cluster = movies_datacluster[movies_datacluster['Cluster'] == user_cluster]

        # Filtrar las películas que el usuario no ha visto
        recommended_movies = movies_in_cluster[~movies_in_cluster['title'].isin(movies_watched_by_user)]

        # Ordenar por 'rating' y devolver las 10 mejores recomendaciones
        recommendations = recommended_movies[['title', 'rating']].sort_values(by='rating', ascending=False).head(10)
        
        pred_to_update['prediction'] = recommendations.to_dict(orient='records')

        return pred_to_update

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# DELETE: Borrar una predicción existente
def delete_prediction(pred_id: int):
    global predictions_db
    predictions_db = [pred for pred in predictions_db if pred['id'] != pred_id]
    return {"message": "Predicción eliminada"}
