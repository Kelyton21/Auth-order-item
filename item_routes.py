from dependencies import get_session
from fastapi import APIRouter, Depends, HTTPException
from schemas import ItemSchema
from models import Item
from dependencies import verificar_token
from models import User

item_router = APIRouter(prefix='/items', tags=['items'])

@item_router.get('/')
async def get_items(Sessao=Depends(get_session), usuario_id = Depends(verificar_token)):
    """
    Endpoint para obter todos os itens cadastrados no banco de dados
    """
    usuario_existe = Sessao.query(User).filter(User.id == usuario_id).first()
    if not usuario_existe:
        raise HTTPException(status_code=401, detail="Usuario não identificado")
    return Sessao.query(Item).all()

@item_router.post('/create')
async def create_item(item: ItemSchema, Sessao=Depends(get_session),usuario_id = Depends(verificar_token)):
    """
    Endpoint para criar um novo item
    """
    usuario_existe = Sessao.query(User).filter(User.id == usuario_id).first()
    if not usuario_existe or usuario_existe.admin == False:
        raise HTTPException(status_code=401, detail="Acesso negado")
    novo_item = Item(name=item.name, price=item.price, size=item.size)
    Sessao.add(novo_item)
    Sessao.commit()
    return {"message": "Item criado com sucesso", "item_id": novo_item.id, "name": novo_item.name}