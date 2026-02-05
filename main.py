from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import shutil
from simplificador import processar_excel
import os
from fastapi.staticfiles import StaticFiles

# Criação da instância do FastAPI
app = FastAPI()

# Montando o diretório estático para servir arquivos como CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates Jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
from fastapi.responses import PlainTextResponse

@app.get("/ads.txt", response_class=PlainTextResponse)
async def ads_txt():
    return "google.com, pub-4284180364619354, DIRECT, f08c47fec0942fa0"


@app.post("/upload")
async def upload_excel(
    file: UploadFile = File(...),
    baseSelecionada: str = Form(...),  # Altere de 'toggle' para 'baseSelecionada'
):
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

    # Processa o arquivo com base na seleção do usuário
    try:
        processar_excel(temp_filename, "saida_simplificada.xlsx", baseSelecionada)  # Use 'baseSelecionada'
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
