from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from fastapi.responses import FileResponse
from .api import router as api_router

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")


@app.get("/")
async def root():
    index_path = os.path.join("public", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return {"error": "index.html no encontrado en la carpeta 'public'"}

app.include_router(api_router)
