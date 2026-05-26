from pydantic import BaseModel, Field
from typing import Optional

# Valida os dados de entrada quando uma empresa for cadastrada
class EmpresaCreate(BaseModel):
    cnpj: str = Field(..., min_length=14, max_length=14, description="CNPJ com 14 dígitos numéricos")
    razao_social: str
    setor_mercado: str

# Valida os dados que a API vai devolver (Response) protegendo o CNPJ
class EmpresaResponse(BaseModel):
    id: int
    cnpj_mascarado: str
    razao_social: str
    setor_mercado: str

    class Config:
        from_attributes = True

# Valida os dados para receber uma nova solicitação de crédito
class SolicitacaoCreditoCreate(BaseModel):
    empresa_id: int
    valor_solicitado: float = Field(..., gt=0, description="O valor deve ser maior que zero")
