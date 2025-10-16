from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DECIMAL, CHAR, DATETIME, Boolean, Date
from db_session import Base 

class ProdutoEstoque(Base):
    __tablename__ = "produtos_estoque"
    __table_args__ = {'schema': 'supply_chain'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True)
    abc: Mapped[str] = mapped_column(CHAR(1), index=True)
    tipo: Mapped[int] = mapped_column(Integer)
    saldo_manut: Mapped[int] = mapped_column(Integer)
    provid_compras: Mapped[int] = mapped_column(Integer)
    recebimento_esperado: Mapped[int] = mapped_column(Integer)
    transito_manut: Mapped[int] = mapped_column(Integer)
    stage_manut: Mapped[int] = mapped_column(Integer)
    recepcao_manut: Mapped[int] = mapped_column(Integer)
    pendente_ri: Mapped[int] = mapped_column(Integer)
    pecas_teste_kit: Mapped[int] = mapped_column(Integer)
    pecas_teste: Mapped[int] = mapped_column(Integer)
    fornecedor_reparo: Mapped[int] = mapped_column(Integer)
    laboratorio: Mapped[int] = mapped_column(Integer)
    wr: Mapped[int] = mapped_column(Integer)
    wrcr: Mapped[int] = mapped_column(Integer)
    stage_wr: Mapped[int] = mapped_column(Integer)
    cmm: Mapped[float] = mapped_column(DECIMAL(10, 2))
    coef_perda: Mapped[float] = mapped_column(DECIMAL(10, 8))
    data_criacao: Mapped[DATETIME] = mapped_column(DATETIME)
    data_atualizacao: Mapped[DATETIME] = mapped_column(DATETIME)
    usuario_criacao: Mapped[str] = mapped_column(String(100), nullable=True)
    usuario_atualizacao: Mapped[str] = mapped_column(String(100), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean)
    
    def __repr__(self) -> str:
        return f"Produto(id={self.id!r}, codigo={self.codigo!r}, cmm={self.cmm!r})"

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'schema': 'supply_chain'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100))
    sobrenome: Mapped[str] = mapped_column(String(100))
    data_nascimento: Mapped[Date] = mapped_column(Date)
    cpf: Mapped[str] = mapped_column(CHAR(11), unique=True)
    funcao: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_senha: Mapped[str] = mapped_column(String(255))
    ativo: Mapped[bool] = mapped_column(Boolean)
    data_criacao: Mapped[DATETIME] = mapped_column(DATETIME)

    def __repr__(self) -> str:
        return f"Usuario(id={self.id!r}, email={self.email!r}, funcao={self.funcao!r})"