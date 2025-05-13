from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import shutil
from simplificador import processar_excel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    with open("{file.filename}.xlsx", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    processar_excel("temp.xlsx", "saida_simplificada.xlsx")
    return FileResponse("saida_simplificada.xlsx", filename="saida_simplificada.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
