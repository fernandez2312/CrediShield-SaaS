import os
import ai_engine
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import models, schemas, security
from database import engine, get_db

# Inicializa a API FastAPI
app = FastAPI(title="CrediShield SaaS - API de Inteligência de Crédito")

# --- MOTOR DE CRÉDITO (Regras de Negócio / Finanças) ---
class CreditEngine:
    @staticmethod
    def analyze(valor_solicitado: float, faturamento_anual: float, divida_total: float) -> str:
        """
        Calcula o risco baseado em regras financeiras básicas:
        1. Se a dívida total + o valor solicitado ultrapassar 60% do faturamento anual, o crédito é RECUSADO.
        2. Caso contrário, é APROVADO.
        """
        limite_comprometimento = faturamento_anual * 0.60
        divida_projetada = divida_total + valor_solicitado

        if divida_projetada > limite_comprometimento:
            return "Recusado"
        return "Aprovado"


# --- ENDPOINTS (Rotas da API) ---

@app.get("/", response_class=HTMLResponse)
def home():
    """
    Renderiza a interface gráfica do usuário (Dashboard UX)
    carregando o arquivo index.html da raiz do projeto.
    """
    caminho_html = "index.html"
    if os.path.exists(caminho_html):
        with open(caminho_html, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Servidor Online</h1><p>Arquivo index.html não encontrado.</p>"


@app.post("/empresas/", response_model=schemas.EmpresaResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    # Aplica a segurança da informação (mascaramento de LGPD)
    cnpj_com_mascara = security.mask_cnpj(empresa.cnpj)
    
    if cnpj_com_mascara == "CNPJ_INVALIDO":
        raise HTTPException(status_code=400, detail="CNPJ inválido. Deve conter 14 dígitos numéricos.")

    # Verifica se o CNPJ já está cadastrado para evitar duplicidade
    db_empresa = db.query(models.Empresa).filter(models.Empresa.cnpj_mascarado == cnpj_com_mascara).first()
    if db_empresa:
        raise HTTPException(status_code=400, detail="Empresa com este CNPJ já cadastrada.")

    # Cria e salva no banco MySQL via ORM
    nova_empresa = models.Empresa(
        cnpj_mascarado=cnpj_com_mascara,
        razao_social=empresa.razao_social,
        setor_mercado=empresa.setor_mercado
    )
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)
    return nova_empresa


@app.post("/credito/solicitar/")
def solicitar_credito(solicitacao: schemas.SolicitacaoCreditoCreate, db: Session = Depends(get_db)):
    # Busca a empresa no banco de dados
    empresa = db.query(models.Empresa).filter(models.Empresa.id == solicitacao.empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    # Busca o balanço financeiro mais recente da empresa
    balanco = db.query(models.BalancoFinanceiro).filter(models.BalancoFinanceiro.empresa_id == empresa.id).first()
    
    # Valores simulados caso a empresa não tenha balanço cadastrado ainda
    faturamento = balanco.faturamento_anual if balanco else 500000.0
    divida = balanco.divida_total if balanco else 50000.0

    # Executa a análise pelo motor matemático clássico
    resultado_status = CreditEngine.analyze(solicitacao.valor_solicitado, faturamento, divida)

    # Executa o parecer inteligente da IA consultando o manual de políticas (RAG)
    parecer_ia = ai_engine.CreditAIEngine.gerar_parecer(
        empresa_nome=empresa.razao_social,
        setor=empresa.setor_mercado,
        valor=solicitacao.valor_solicitado,
        faturamento=faturamento,
        divida=divida,
        status_motor=resultado_status
    )

    # Registra a decisão na tabela do MySQL
    nova_solicitacao = models.SolicitacaoCredito(
        empresa_id=solicitacao.empresa_id,
        valor_solicitado=solicitacao.valor_solicitado,
        status=resultado_status
    )
    db.add(nova_solicitacao)
    db.commit()
    db.refresh(nova_solicitacao)

    return {
        "mensagem": "Análise de crédito integrada com IA concluída com sucesso.",
        "empresa": empresa.razao_social,
        "setor": empresa.setor_mercado,
        "valor_solicitado": solicitacao.valor_solicitado,
        "score_matematico": resultado_status,
        "parecer_auditoria_ia": parecer_ia,
        "protocolo_id": nova_solicitacao.id
    }
