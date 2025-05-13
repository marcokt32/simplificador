from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import shutil
from simplificador import processar_excel
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    temp_filename = "temp.xlsx"

    # Salva o arquivo no disco
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o arquivo: {str(e)}")

    # Verifica se o arquivo foi salvo
    if not os.path.exists(temp_filename):
        raise HTTPException(status_code=500, detail="Arquivo não foi salvo corretamente.")

    # Processa o arquivo salvo
    try:
        processar_excel(temp_filename, "saida_simplificada.xlsx")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o Excel: {str(e)}")
    finally:
        # Remove arquivo temporário, mesmo que ocorra erro
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    # Retorna o arquivo final para download
    return FileResponse(
        "saida_simplificada.xlsx",
        filename="saida_simplificada.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )