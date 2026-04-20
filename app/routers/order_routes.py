from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.dependecies import pegar_sessao
from app.schemas.schemas import PedidoSchema
from app.models.models import Pedido

order_router = APIRouter(prefix="/pedidos", tags = ["Pedidos"])

@order_router.get("/",summary="Home")
async def pedidos():
    """ Rota padrao de pedidos"""
    return {"mensagem": "voce acessou a rota de pedidos"}


@order_router.post("/pedido",summary="criação do pedido")
async def criar_pedido(pedido_schema: PedidoSchema, Session = Depends(pegar_sessao)):
        novo_pedido = Pedido(usuario=pedido_schema.usuario)
        Session.add(novo_pedido)
        Session.commit()
        return {
            "mensagem": f"Pedido criado com sucesso! ID do pedido: {novo_pedido.id} e o status do pedido é {novo_pedido.status}"
        }
