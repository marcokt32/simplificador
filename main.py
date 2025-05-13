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
    temp_filename = "temp.xlsx"

    # Salva o upload como 'temp.xlsx'
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Processa o arquivo
    processar_excel(temp_filename, "saida_simplificada.xlsx")

    # Remove o arquivo temporário, se quiser limpar
    #os.remove(temp_filename)

    # Retorna o arquivo processado para download
    return FileResponse(
        "saida_simplificada.xlsx",
        filename="saida_simplificada.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )