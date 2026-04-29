from dependencies import get_session, bcrypt_context, verificar_token
from models import User
from fastapi import Depends, APIRouter, HTTPException
from schemas import UserSchema, LoginSchema
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix='/auth', tags=['auth'])

def create_token(id_user,duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dicionario_info = {
        "sub": str(id_user),
        "exp": data_expiracao
    }
    token = jwt.encode(dicionario_info, SECRET_KEY, algorithm=ALGORITHM)
    return token

def authenticate_user(senha,email,Sessao):
    usuario_existe = Sessao.query(User).filter(User.email==email).first()
    if usuario_existe and bcrypt_context.verify(senha, usuario_existe.password):
        return usuario_existe
    return None

@auth_router.post('/login')
async def get_auth(usuario: LoginSchema, Sessao=Depends(get_session)):
    """
    Endpoint para autenticação de usuários
    """

    usuario = authenticate_user(usuario.password, usuario.email, Sessao)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não cadastrado")
    else:
        access_token = create_token(usuario.id)
        refresh_token = create_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }

@auth_router.post('/login-form')
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), Sessao=Depends(get_session)):
    """
    Endpoint para autenticação de usuários via formulário
    """

    usuario = authenticate_user(dados_formulario.password, dados_formulario.username, Sessao)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não cadastrado")
    else:
        access_token = create_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }
        
        

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

@auth_router.get('/refresh')
async def refresh(usuario_id:int = Depends(verificar_token)):
    token = create_token(usuario_id)
    return {
        "access_token": token,
        "token_type": "bearer"
        }