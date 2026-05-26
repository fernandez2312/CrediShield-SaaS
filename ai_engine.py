import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configura a API do Google Gemini usando a chave do .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class CreditAIEngine:
    @staticmethod
    def _recuperar_manual_politicas() -> str:
        """
        Simula a etapa de Recuperação (RAG) lendo o arquivo local 
        de políticas de conformidade para injetar no contexto da IA.
        """
        caminho_arquivo = "politicas_credito.md"
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                return f.read()
        return "Nenhum manual de políticas internas disponível."

    @classmethod
    def gerar_parecer(cls, empresa_nome: str, setor: str, valor: float, faturamento: float, divida: float, status_motor: str) -> str:
        """
        Combina o contexto do manual recuperado com os dados da solicitação
        para gerar uma análise de risco e compliance em linguagem natural.
        """
        # Etapa de recuperação do contexto (RAG)
        manual_contexto = cls._recuperar_manual_politicas()

        # Configura o modelo (usando o flash, ideal para aplicações rápidas e APIs de baixa latência)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Monta a engenharia de prompt avançada contextualizada (Garante governança)
        prompt = f"""
        Você é um Analista de Risco Sênior do sistema CrediShield SaaS.
        Sua tarefa é emitir um parecer executivo profissional e direto (máximo de 3 parágrafos) sobre um pedido de crédito, baseado rigorosamente no manual de conformidade fornecido.

        --- MANUAL DE CONFORMIDADE INTERNA DA EMPRESA ---
        {manual_contexto}

        --- DADOS DA SOLICITAÇÃO ATUAL ---
        Empresa: {empresa_nome}
        Setor de Mercado: {setor}
        Valor do Crédito Solicitado: R$ {valor:,.2f}
        Faturamento Anual informado: R$ {faturamento:,.2f}
        Dívida Total atual da empresa: R$ {divida:,.2f}
        Resultado do Cálculo de Score Automático: {status_motor}

        --- INSTRUÇÕES DO PARECER ---
        Analise se o pedido fere alguma cláusula setorial ou de restrição de tempo/teto do manual anexado. 
        Mesmo que o score automático dê 'Aprovado', avalie se as regras de conformidade e o comprometimento geram algum alerta ou contraindicação técnica. Seja direto, formal e objetivo.
        """

        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Erro ao gerar parecer de IA: {str(e)}. Processamento manual recomendado."
