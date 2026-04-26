from database import engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_session():
    try:
        ConexaoBanco = sessionmaker(bind=engine)
        Sessao = ConexaoBanco()
        yield Sessao
    finally:
        Sessao.close()