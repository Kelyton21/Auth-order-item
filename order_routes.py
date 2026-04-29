from models import User
from dependencies import get_session
from fastapi import APIRouter, Depends, HTTPException
from schemas import OrderSchema
from models import Order, Item, OrderItem


order_router = APIRouter(prefix='/orders', tags=['orders'])

@order_router.get('/')
async def get_orders(Sessao=Depends(get_session)):
    """
    Endpoint para obter todos os pedidos cadastrados no banco de dados
    """
    return Sessao.query(Order).all()

@order_router.post('/create')
async def create_order(pedido: OrderSchema, Sessao=Depends(get_session)):
    """
    Endpoint para criar um pedido
    """
    usuario_existe = Sessao.query(User).filter(User.id == pedido.user_id).first()
    
    if usuario_existe:
        novo_pedido = Order(user_id=pedido.user_id,total=0.0,status=pedido.status)
        Sessao.add(novo_pedido)
        Sessao.flush()
        total_geral = 0.0

        for item in pedido.items:
            produto = Sessao.query(Item).filter(Item.id == item.item_id).first()
            if not produto:
                raise HTTPException(status_code=404, detail=f"Produto {item.item_id} não encontrado")
            total_item = produto.price * item.quantity
            total_geral += total_item

            novo_item_pedido = OrderItem(
            order_id=novo_pedido.id,
            item_id=produto.id,
            quantity=item.quantity,
            total=total_item
            )

            Sessao.add(novo_item_pedido)

        novo_pedido.total = total_geral
        Sessao.commit()
        
        return {"message": "Pedido criado com sucesso", "order_id": novo_pedido.id, "total": total_geral}
    else:
        raise HTTPException(status_code=400, detail="Erro na criacao do Pedido")
