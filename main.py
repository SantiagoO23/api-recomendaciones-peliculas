from fastapi import FastAPI
from routes import configure_routes

app = FastAPI()

#configurar rutas
configure_routes(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0",port=5500)