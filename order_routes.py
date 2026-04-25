from fastapi import APIRouter

order_router = APIRouter(prefix='/orders', tags=['orders'])

@order_router.get('/')
async def get_orders():
    """
    Endpoint para pedidos
    """
    return {'message': 'Orders'}