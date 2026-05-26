from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    cnpj_mascarado = Column(String(255), unique=True, nullable=False, index=True)
    razao_social = Column(String(255), nullable=False)
    setor_mercado = Column(String(100), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos (ORM mapeia automaticamente as tabelas filhas)
    balancos = relationship("BalancoFinanceiro", back_populates="empresa", cascade="all, delete-orphan")
    solicitacoes = relationship("SolicitacaoCredito", back_populates="empresa", cascade="all, delete-orphan")


class BalancoFinanceiro(Base):
    __tablename__ = "balancos_financeiros"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    ano_fiscal = Column(Integer, nullable=False)
    faturamento_anual = Column(Float, nullable=False)
    divida_total = Column(Float, nullable=False)
    ativo_circulante = Column(Float, nullable=False)
    passivo_circulante = Column(Float, nullable=False)

    empresa = relationship("Empresa", back_populates="balancos")


class SolicitacaoCredito(Base):
    __tablename__ = "solicitacoes_credito"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    valor_solicitado = Column(Float, nullable=False)
    status = Column(String(50), default="Pendente")  # Pendente, Aprovado, Recusado
    data_solicitacao = Column(DateTime, default=datetime.utcnow)

    empresa = relationship("Empresa", back_populates="solicitacoes")
