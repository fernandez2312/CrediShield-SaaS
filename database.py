import os
from urllib.parse import quote_plus  # <--- Adicione esta linha no topo
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Carrega as variáveis do arquivo .env
load_dotenv()

# Resgata as credenciais de forma segura do ambiente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Protege os caracteres especiais da senha (como o @)
PASSWORD_ESCAPED = quote_plus(DB_PASSWORD) # <--- Adicione esta linha

# Monta a URL usando a senha protegida
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{PASSWORD_ESCAPED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cria o motor de conexão
engine = create_engine(DATABASE_URL)

# Configura a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
