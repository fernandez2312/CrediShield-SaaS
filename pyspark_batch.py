import os
import json
from datetime import datetime

print("⚡ [Databricks/Spark Simulation] Inicializando processamento de dados...")

def rodar_pipeline_medallion():
    # 1. Camada BRONZE (Dados Brutos Extraídos da API/Banco)
    print("📦 Camada BRONZE: Lendo logs brutos de solicitações de crédito...")
    dados_brutos = [
        {"id": 1, "empresa": "AutoParts SA", "valor": 250000.0, "status": "Aprovado", "data": "2026-05-26"},
        {"id": 2, "empresa": "TechLinear LTDA", "valor": 90000.0, "status": "Recusado", "data": "2026-05-26"},
        {"id": 3, "empresa": "VarejoTotal Conf", "valor": 45000.0, "status": "Aprovado", "data": "2026-05-26"},
        {"id": 4, "empresa": "AutoParts SA", "valor": None, "status": "Erro", "data": "2026-05-26"}, # Dado corrompido
    ]
    
    # 2. Camada SILVER (Limpeza e Padronização dos Dados)
    print("🧹 Camada SILVER: Filtrando registros corrompidos e tratando nulos...")
    dados_limpos = [d for d in dados_brutos if d["valor"] is not None and d["status"] != "Erro"]
    
    # 3. Camada GOLD (Agregação de Negócio para Diretores e BI)
    print("🥇 Camada GOLD: Gerando KPI consolidado de crédito aprovado por empresa...")
    kpi_empresas = {}
    for registro in dados_limpos:
        if registro["status"] == "Aprovado":
            nome = registro["empresa"]
            kpi_empresas[nome] = kpi_empresas.get(nome, 0.0) + registro["valor"]
            
    # Salva o resultado final da camada Gold
    with open("camada_gold_analytics.json", "w", encoding="utf-8") as f:
        json.dump(kpi_empresas, f, indent=4, ensure_ascii=False)
        
    print("✅ Pipeline Medallion executada com sucesso! Resultados salvos em 'camada_gold_analytics.json'")
    print("📊 Resumo de Crédito Concedido:", kpi_empresas)

if __name__ == "__main__":
    rodar_pipeline_medallion()
