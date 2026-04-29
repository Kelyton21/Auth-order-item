from dependencies import get_session
from fastapi import APIRouter, Depends, HTTPException
from schemas import ItemSchema
from models import Item

item_router = APIRouter(prefix='/items', tags=['items'])

@item_router.get('/')
async def get_items(Sessao=Depends(get_session)):
    """
    Endpoint para obter todos os itens cadastrados no banco de dados
    """
    return Sessao.query(Item).all()

@item_router.post('/create')
async def create_item(item: ItemSchema, Sessao=Depends(get_session)):
    """
    Endpoint para criar um novo item
    """
    novo_item = Item(name=item.name, price=item.price, size=item.size)
    Sessao.add(novo_item)
    Sessao.commit()
    return {"message": "Item criado com sucesso", "item_id": novo_item.id, "name": novo_item.name}