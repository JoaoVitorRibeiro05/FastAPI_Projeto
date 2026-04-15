from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags = ["orders"])

@order_router.get("/")
async def pedidos():
    """ Rota padrao de pedidos"""
    return {"mensagem": "voce acessou a rota de pedidos"}

@order_router.post("/criar_pedidos")
async def Criar_pedidos():
    
    return {"mensagem": "Digite o nome do pedido"}

