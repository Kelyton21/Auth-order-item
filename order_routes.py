from typing import List
from sqlalchemy.orm import joinedload
from models import User
from dependencies import get_session
from fastapi import APIRouter, Depends, HTTPException
from schemas import OrderSchema, OrderResponse
from models import Order, Item, OrderItem
from dependencies import verificar_token

order_router = APIRouter(prefix='/orders', tags=['orders'],dependencies=[Depends(verificar_token)])
    
@order_router.get('/', response_model=List[OrderResponse])
async def get_orders(Sessao=Depends(get_session),usuario_id = Depends(verificar_token)):
    """
    Endpoint para obter todos os pedidos cadastrados no banco de dados
    """
    usuario = Sessao.query(User).filter(User.id==usuario_id).first()
    existe_pedido = Sessao.query(Order).filter(Order.user_id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario {usuario_id} não encontrado")
    if usuario.admin == True:
        return Sessao.query(Order).options(joinedload(Order.items).joinedload(OrderItem.item)).all()
    if not existe_pedido:
        raise HTTPException(status_code=404, detail=f"Nenhum pedido encontrado para o usuario {usuario_id}")
    else:
        return Sessao.query(Order).options(joinedload(Order.items).joinedload(OrderItem.item)).filter(Order.user_id==usuario_id).all()

@order_router.post('/create')
async def create_order(pedido: OrderSchema, Sessao=Depends(get_session),usuario_id = Depends(verificar_token)):
    """
    Endpoint para criar um pedido
    """
    usuario_existe = Sessao.query(User).filter(User.id == usuario_id).first()
    
    if usuario_existe:
        novo_pedido = Order(user_id=usuario_id,total=0.0,status=pedido.status)
        Sessao.add(novo_pedido)
        Sessao.flush() # "comunica" ao banco de dados as mudanças feitas no código, mas sem encerrar a transação
        total_geral = 0.0

        for item in pedido.items:
            produto = Sessao.query(Item).filter(Item.id == item.item_id).first()
            if not produto:
                raise HTTPException(status_code=404, detail=f"Produto {item.item_id} não encontrado")
            total_item = item.calculate_total(produto.price)
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

@order_router.delete("/{order_id}")
async def delete_order(order_id: int,Sessao=Depends(get_session),usuario_id = Depends(verificar_token)):
    # verificar se o pedido pertence ao usuario 
    # verificar se o user é admin
    pedido = Sessao.query(Order).filter(Order.id==order_id).first()
    usuario = Sessao.query(User).filter(User.id==usuario_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail=f"Pedido {order_id} não encontrado")
    if usuario_id != pedido.user_id and not usuario.admin:
        raise HTTPException(status_code=401, detail="Acesso negado")

    pedido.status = "CANCELADO"
    Sessao.commit()
    return {"status":pedido.status,"message": f"Pedido {order_id} cancelado com sucesso"}

@order_router.post("/{order_id}/add-item")
async def add_item_to_order(order_id: int, item_adicional: OrderItemCreate, Sessao=Depends(get_session), usuario_id = Depends(verificar_token)):
    """
    Endpoint para adicionar um item a um pedido existente
    """
    pedido = Sessao.query(Order).filter(Order.id == order_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.status != "PENDENTE":
        raise HTTPException(status_code=400, detail="Não é possível alterar um pedido que não esteja pendente")

    if pedido.user_id != usuario_id:
        raise HTTPException(status_code=401, detail="Acesso negado: este pedido não pertence a você")

    produto = Sessao.query(Item).filter(Item.id == item_adicional.item_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    total_novo_item = item_adicional.calculate_total(produto.price)
    novo_item_pedido = OrderItem(
        order_id=pedido.id,
        item_id=produto.id,
        quantity=item_adicional.quantity,
        total=total_novo_item
    )
    Sessao.add(novo_item_pedido)
    pedido.total += total_novo_item
    Sessao.commit()
    return {
        "message": "Item adicionado com sucesso", 
        "order_id": pedido.id, 
        "item_adicionado": produto.name,
        "novo_total_pedido": pedido.total
    }
