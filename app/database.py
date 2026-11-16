"""Conexão com o PostgreSQL usando SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

# engine: a "ponte" entre o Python e o banco
engine = create_engine(DATABASE_URL)

# SessionLocal: fábrica de sessões. Cada requisição ganha a sua.
# autocommit=False -> só grava no banco quando chamarmos db.commit()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: classe mãe de todos os models (as tabelas vão herdar dela)
Base = declarative_base()


def get_db():
    """Abre uma sessão para a rota e garante que ela fecha no final."""
    db = SessionLocal()
    try:
        yield db  # entrega a sessão para a rota usar
    finally:
        db.close()  # roda sempre, mesmo se a rota der erro
