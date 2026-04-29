from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from item_routes import item_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(item_router)

