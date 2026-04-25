from fastapi import APIRouter

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
async def get_auth():
    """
    Endpoint para autenticação
    """
    return {'message': 'Auth', 'autenticant': True}