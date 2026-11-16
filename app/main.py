"""Ponto de entrada da API. Rodar com: uvicorn app.main:app --reload"""
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

app = FastAPI(
    title="API Loja de Roupas",
    description="API REST para gerenciar uma loja de roupas online.",
    version="0.1.0",
)


@app.get("/")
def raiz():
    return {"mensagem": "API Loja de Roupas no ar", "docs": "/docs"}


@app.get("/health")
def health(db: Session = Depends(get_db)):
    """Confere se a API consegue falar com o banco."""
    try:
        db.execute(text("SELECT 1"))  # consulta mínima, só para testar a conexão
    except Exception:
        # 503 = serviço indisponível (o servidor está ok, mas depende de algo que caiu)
        raise HTTPException(status_code=503, detail="Banco de dados indisponível")
    return {"status": "ok", "banco": "conectado"}
