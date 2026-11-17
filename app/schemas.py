"""Schemas (Pydantic): definem o formato do JSON que entra e que sai da API.

Padrão usado em cada entidade:
- XCreate: o que o cliente da API ENVIA para criar (POST) ou substituir (PUT)
- XUpdate: tudo opcional, para alterar só alguns campos (PATCH)
- XOut:    o que a API DEVOLVE (inclui o id)
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------- Categoria ----------
class CategoriaCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=50)
    descricao: Optional[str] = Field(default=None, max_length=200)


class CategoriaUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=2, max_length=50)
    descricao: Optional[str] = Field(default=None, max_length=200)


class CategoriaOut(CategoriaCreate):  # herda nome e descricao, e acrescenta o id
    id: int
    # Permite montar o schema a partir de um objeto do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


# ---------- Produto ----------
class ProdutoCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=300)
    tamanho: str = Field(min_length=1, max_length=5)
    preco: float = Field(gt=0)  # gt = "greater than": maior que 0
    estoque: int = Field(default=0, ge=0)  # ge = "greater or equal": 0 ou mais
    categoria_id: int


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=2, max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=300)
    tamanho: Optional[str] = Field(default=None, min_length=1, max_length=5)
    preco: Optional[float] = Field(default=None, gt=0)
    estoque: Optional[int] = Field(default=None, ge=0)
    categoria_id: Optional[int] = None


class ProdutoOut(ProdutoCreate):
    id: int
    categoria: CategoriaOut  # schema aninhado: a categoria vem completa no JSON
    model_config = ConfigDict(from_attributes=True)


# ---------- Endereço (1:1 com Cliente) ----------
class EnderecoCreate(BaseModel):
    rua: str = Field(min_length=2, max_length=150)
    numero: str = Field(min_length=1, max_length=10)
    bairro: str = Field(min_length=2, max_length=80)
    cidade: str = Field(min_length=2, max_length=80)
    estado: str = Field(min_length=2, max_length=2)  # sigla: RJ, SP...
    cep: str = Field(min_length=8, max_length=9)


class EnderecoOut(EnderecoCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------- Cliente ----------
class ClienteCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=100)
    telefone: Optional[str] = Field(default=None, max_length=20)
    endereco: EnderecoCreate  # o cliente já é criado junto com o endereço


class ClienteUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=2, max_length=100)
    email: Optional[str] = Field(default=None, min_length=5, max_length=100)
    telefone: Optional[str] = Field(default=None, max_length=20)
    endereco: Optional[EnderecoCreate] = None


class ClienteOut(BaseModel):
    id: int
    nome: str
    email: str
    telefone: Optional[str] = None
    endereco: Optional[EnderecoOut] = None
    model_config = ConfigDict(from_attributes=True)


# ---------- Pedido e itens (N:N) ----------
class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)


class PedidoCreate(BaseModel):
    cliente_id: int
    itens: List[ItemPedidoCreate] = Field(min_length=1)  # pelo menos 1 item


class ItemPedidoOut(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float
    subtotal: float  # vem do @property do model
    model_config = ConfigDict(from_attributes=True)


class PedidoOut(BaseModel):
    id: int
    data: datetime
    status: str
    cliente_id: int
    itens: List[ItemPedidoOut]
    total: float  # vem do @property do model
    model_config = ConfigDict(from_attributes=True)
