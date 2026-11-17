"""Models: cada classe vira uma tabela no PostgreSQL."""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, nullable=False)
    descricao = Column(String(200))

    # 1:N -> uma categoria tem vários produtos
    produtos = relationship("Produto", back_populates="categoria")


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(300))
    tamanho = Column(String(5), nullable=False)  # P, M, G, GG...
    # Numeric(10, 2): número exato com 2 casas. Dinheiro não usa float!
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False, default=0)

    # Chave estrangeira: o lado "N" do 1:N guarda o id do lado "1"
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    categoria = relationship("Categoria", back_populates="produtos")
    itens = relationship("ItemPedido", back_populates="produto")


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(20))

    # 1:1 -> uselist=False devolve UM endereço, não uma lista
    # cascade: apagou o cliente, apaga o endereço junto
    endereco = relationship(
        "Endereco",
        back_populates="cliente",
        uselist=False,
        cascade="all, delete-orphan",
    )
    # 1:N -> um cliente tem vários pedidos (sem cascade: histórico de vendas não some)
    pedidos = relationship("Pedido", back_populates="cliente")


class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True)
    rua = Column(String(150), nullable=False)
    numero = Column(String(10), nullable=False)
    bairro = Column(String(80), nullable=False)
    cidade = Column(String(80), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(9), nullable=False)

    # unique=True garante o 1:1 no próprio banco: um cliente, um endereço
    cliente_id = Column(Integer, ForeignKey("clientes.id"), unique=True, nullable=False)

    cliente = relationship("Cliente", back_populates="endereco")


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True)
    data = Column(DateTime, nullable=False, default=datetime.now)
    status = Column(String(20), nullable=False, default="criado")  # "criado" ou "cancelado"

    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="pedidos")
    # Os itens só existem dentro do pedido: apagou o pedido, apaga os itens
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

    @property
    def total(self):
        """Calculado na hora, não é coluna no banco."""
        return sum(item.subtotal for item in self.itens)


class ItemPedido(Base):
    """Tabela intermediária do N:N entre Pedido e Produto."""

    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    # Preço copiado no momento da compra: se o produto mudar de preço depois,
    # o pedido antigo continua com o valor que o cliente pagou
    preco_unitario = Column(Numeric(10, 2), nullable=False)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")

    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade


class Usuario(Base):
    """Administrador que faz login (usado na etapa de autenticação)."""

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(200), nullable=False)  # nunca a senha pura
