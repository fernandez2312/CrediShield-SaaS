# 🛡️ CrediShield SaaS — Inteligência Financeira & Análise de Risco com IA Generativa

O **CrediShield SaaS** é uma plataforma corporativa ponta a ponta (End-to-End) projetada para automatizar o processo de concessão e auditoria de risco de crédito para empresas. A aplicação combina regras financeiras matemáticas clássicas à flexibilidade da Inteligência Artificial Generativa via Arquitetura RAG (Retrieval-Augmented Generation).

O projeto adota práticas rigorosas de segurança de dados (LGPD), governança ágil e engenharia de dados em camadas (Arquitetura Medallion).

---

## 🚀 Estrutura do Projeto e Execução em 5 Sprints

O desenvolvimento do produto foi estruturado seguindo o modelo de gerenciamento ágil (Scrum/Kanban):

### 📌 Sprint 1: Governança, Infraestrutura e Banco de Dados (MySQL)
*   **Gestão Ágil**: Configuração do fluxo de trabalho e cartões de tarefas utilizando o Notion para tracking de progresso.
*   **Modelagem de Dados**: Criação do banco de dados relacional `credishield` mapeando as entidades através do ORM SQLAlchemy:
    *   `empresas`: Cadastro principal com indexação de chaves.
    *   `balancos_financeiros`: Dados contábeis (faturamento, dívidas, ativos e passivos circulantes).
    *   `solicitacoes_credito`: Registro de transações, valores e status de auditoria.
*   **Segurança da Informação**: Implementação de variáveis de ambiente (`.env`) para isolar credenciais críticas de acesso do banco e tratamentos especiais de caracteres.

### 📌 Sprint 2: Backend de Alta Performance & Validação (FastAPI)
*   **Servidor REST**: Construção do core da API assíncrona utilizando FastAPI e servidor Uvicorn com hot-reload.
*   **Esquemas de Validação**: Implementação de validação rigorosa de payloads de entrada e saída de dados com Pydantic (`schemas.py`).
*   **Regras de Negócio**: Criação do motor matemático clássico focado em indicadores de contabilidade e finanças corporativas, avaliando o comprometimento de renda projetado sobre o faturamento.
### 📌 Sprint 3: O Cérebro de IA com Arquitetura RAG (Gemini)
*   **Base de Conhecimento**: Criação de um repositório de diretrizes corporativas em Markdown contendo regras setoriais de compliance e travas de segurança regulatórias.
*   **Recuperação e Prompting (RAG)**: Desenvolvimento de um motor de IA inteligente que lê o manual de conformidade em tempo real, cruza com os dados financeiros do MySQL e injeta o contexto no modelo generativo estável `gemini-2.5-flash`.
*   **Resultados Autónomos**: O sistema gera um parecer executivo sênior humanizado justificando riscos e salvando o log de auditoria diretamente nas tabelas relacionais.

### 📌 Sprint 4: Interface de Usuário & Métricas de Produto (Dashboard UX)
*   **Frontend Customizado**: Construção de uma página web responsiva e limpa do zero utilizando HTML avançado e CSS moderno focado em experiência do usuário (UX), eliminando frameworks pesados para valorizar a velocidade de renderização.
*   **Consumo Assíncrono de APIs**: Integração completa da interface com as rotas do backend através de requisições assíncronas assentes em JavaScript (`Fetch API`), exibindo transições de carregamento (loading states) fluidas enquanto a IA processa o parecer.
*   **Métricas de Growth**: Inclusão de scripts de monitoramento de eventos simulando tags de produto do Google Analytics para rastrear cliques em botões de conversão e jornadas do usuário.

### 📌 Sprint 5: Analytics, Engenharia de Big Data (Medallion) e Deploy
*   **Pipeline de Big Data**: Script em Python puro simulando uma esteira de dados em lote no ecossistema Databricks, organizando logs brutos de auditoria rigorosamente entre as camadas Bronze (dados brutos), Silver (limpeza de corrupções) e Gold (geração de KPIs consolidados em tabelas analíticas).
*   **Versionamento**: Estruturação semântica de commits no repositório Git e publicação do portfólio completo na nuvem do GitHub.

---

## 🛠️ Stack Técnica Empregada

*   **Linguagem Principal**: Python
*   **Framework de API**: FastAPI & Uvicorn
*   **Banco de Dados**: MySQL & SQLAlchemy ORM
*   **Inteligência Artificial**: Google Gemini API & Engenharia de Prompt (RAG)
*   **Frontend & UX**: HTML5, CSS3, JavaScript Avançado e Conceitos de UX Design
*   **Engenharia de Dados**: Lógica de Dataframes e Arquitetura Medallion (Bronze/Silver/Gold)
*   **Gestão & Growth**: Metodologias Ágeis (Notion Kanban), Git e Google Analytics Tracking

---

## 🚀 Como Executar a Aplicação Localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd CrediShield-SaaS
   ```

2. **Configure o Ambiente Virtual e as Dependências:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install fastapi uvicorn sqlalchemy pymysql python-dotenv pydantic google-generativeai
   ```

3. **Configure as Variáveis de Ambiente:**
   Crie um arquivo `.env` na raiz do projeto com as credenciais do seu MySQL local e sua chave gerada no Google AI Studio:
   ```text
   DB_USER=seu_usuario_root
   DB_PASSWORD=sua_senha_do_mysql
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=credishield
   GEMINI_API_KEY=sua_chave_do_gemini
   ```

4. **Inicie o Servidor Backend:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Acesse a Aplicação:**
   Abra o seu navegador de preferência e digite: `http://127.0.0` para interagir diretamente com a interface gráfica!
