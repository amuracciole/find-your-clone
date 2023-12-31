from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from functions import *


app = FastAPI()

# Agregar el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def index():
    #index_path = Path("index.html")
    #return FileResponse(index_path)
    return {"message": "pagina principal"}

@app.post("/upload/{name}")
async def upload_file(name: str, file: UploadFile):
    with open(f"/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/you_photo/photo.jpg", "wb") as f:
        f.write(file.file.read())
    #return {"filename": file.filename, "content_type": file.content_type}
    try:
        result = mainFunction(name)
        return {"message": result}
    except Exception as e:
        return {"error": str(e)}