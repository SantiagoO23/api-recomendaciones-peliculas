from controllers.prediccion_controllers import get_predictions, create_prediction, update_prediction, delete_prediction

def configure_routes(app):
    # Ruta GET para obtener predicciones pasadas
    app.get("/predicciones")(get_predictions)
    
    # Ruta POST para hacer una nueva predicción
    app.post("/predicciones")(create_prediction)
    
    # Ruta PUT para actualizar una predicción existente
    app.put("/predicciones/{pred_id}")(update_prediction)
    
    # Ruta DELETE para eliminar una predicción
    app.delete("/predicciones/{pred_id}")(delete_prediction)
