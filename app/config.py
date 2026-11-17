"""Lê as configurações do arquivo .env (nada de senha dentro do código)."""
import os

from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente do programa
load_dotenv()

# O "" é o valor padrão se a variável não existir.
# Assim DATABASE_URL é sempre texto (str), nunca None.
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Falha cedo e com mensagem clara, em vez de um erro estranho mais tarde
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL não definida. Copie .env.example para .env e ajuste os valores."
    )
