import os
from sqlalchemy import create_engine # Conexão com o banco de dados
from sqlalchemy.ext.declarative import declarative_base # Base para os modelos para a criação do banco de dados
from sqlalchemy.orm import sessionmaker # Fábrica de sessões
from dotenv import load_dotenv # Carregar variáveis do .env

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# 2. Pega a URL do banco de dados
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Cria o motor de conexão (Engine)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. Cria a fábrica de sessões (para fazer consultas)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Classe base para os seus modelos (tabelas)
Base = declarative_base()

# Função utilitária para obter a conexão nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()