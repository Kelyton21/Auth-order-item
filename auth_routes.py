from dependencies import get_session, bcrypt_context
from models import User
from fastapi import Depends, APIRouter, HTTPException
from schemas import UserSchema


auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
async def get_auth():
    """
    Endpoint para autenticação
    """
    return {'message': 'Auth', 'autenticant': True}

@auth_router.post('/register')
async def register(usuario: UserSchema, Sessao=Depends(get_session)):
    """
    Endpoint para registrar um novo usuário
    """
    usuario_existe = Sessao.query(User).filter(User.email==usuario.email).first()

    if usuario_existe:
        raise HTTPException(status_code=400, detail="Usuario já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario.password)
        novo_usuario = User(usuario.name, usuario.email, senha_criptografada)
        Sessao.add(novo_usuario)
        Sessao.commit()
        raise HTTPException(status_code=200, detail= f"Usuario {usuario.email} cadastrado com sucesso!")

    