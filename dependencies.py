from database import engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from config import SECRET_KEY, ALGORITHM, oauth2_schema
from jose import jwt, JWTError
from models import User
from fastapi import Depends, HTTPException

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_session():
    try:
        ConexaoBanco = sessionmaker(bind=engine)
        Sessao = ConexaoBanco()
        yield Sessao
    finally:
        Sessao.close()

def verificar_token(token: str = Depends(oauth2_schema),Sessao=Depends(get_session)):
    #verificar se o token é valido
    # extrair o id do usuario do token
    try:
        dicionario = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado")
    
    usuario = Sessao.query(User).filter(User.id==dicionario['sub']).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso invalido")
    return usuario.id