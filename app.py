from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from find_your_clone import *


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
    return {"message": "pagina principal"}

@app.post("/upload/")
async def upload_file(file: UploadFile):
    with open(f"/Users/andresmuracciole/Desktop/Proyectos/find_your_clone/you_photo/photo.jpg", "wb") as f:
        f.write(file.file.read())
    #return {"filename": file.filename, "content_type": file.content_type}
    try:
        result = mainFunction()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}