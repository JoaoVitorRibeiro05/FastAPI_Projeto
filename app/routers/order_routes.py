from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.dependecies import pegar_sessao,verificar_token
from app.schemas.schemas import PedidoSchema,ItemPedidoSchema
from app.models.models import Pedido,Usuario,ItensPedidos

order_router = APIRouter(prefix="/pedidos", tags = ["Pedidos"],dependencies=[Depends(verificar_token)])

@order_router.get("/",summary="Home")
async def pedidos():
    """ Rota padrao de pedidos"""
    return {"mensagem": "voce acessou a rota de pedidos"}


@order_router.post("/pedido",summary="criação do pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session:Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
        usuario_no_banco = session.query(Usuario).filter(Usuario.id == pedido_schema.usuario).first() # verificar se o usuário existe no banco
        
        if not usuario_no_banco: # senao existir usuário no banco
              raise HTTPException(status_code=401, detail="Usuário não encontrado!")
        
        novo_pedido = Pedido(usuario=pedido_schema.usuario)
        session.add(novo_pedido)
        session.commit()
        return {
            "mensagem": f"Pedido criado com sucesso! ID do pedido: {novo_pedido.id} e o status do pedido é {novo_pedido.status}"
        }
      
@order_router.post("/pedido/cancelar/{id_pedido}",summary="Cancelar Pedido")
async def cancelar_pedido(id_pedido: int,session:Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
      # usuario.admin = True
      # usuario.id = pedido.usuario
      pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
      if not pedido:
            raise HTTPException(
                  status_code=404,
                  detail= "Pedido não encontrado!"
            )
      if not usuario.admin and usuario.id != pedido.usuario: # se o usuario não for adm e o id dele for diferente do dono do pedido 
            raise HTTPException(status_code=401,detail="Voce não tem autorização para cancelar o pedido!")
      
      pedido.status = "CANCELADO"
      session.commit()
      return {
            "mensagem": f"Pedido numero: {pedido.id} cencalado com sucesso!", # processo de Lazyloaded
            "pedido": pedido
      }

# endpoint para deletar pedido
@order_router.delete("/pedido/deletar_pedido/{id_pedido}",summary="Deletando Pedido")
async def deletar_pedido(id_pedido: int, session:Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
        pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
        if not pedido:
            raise HTTPException(
                  status_code=404,
                  detail= "Pedido não encontrado!"
            )
        if not usuario.admin and usuario.id != pedido.usuario: # se o usuario não for adm e o id dele for diferente do dono do pedido 
            raise HTTPException(status_code=401, detail="Voce não tem autorização para deletar o pedido!")
        session.delete(pedido) # deletando pedido
        session.commit()
        return {
              "mensagem" : f"Pedido {pedido.id} deletado com sucesso!",
              "pedido" : pedido
        }

@order_router.get("/listar", summary="Listar pedidos")
async def listar_pedidos(session:Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
      if not usuario.admin:
             raise HTTPException(status_code=401, detail="Voce não tem autorização para listar os pedidos!")

      else:
            pedidos = session.query(Pedido).all()
            return {
                  "Pedidos": pedidos
            }

@order_router.post("/pedido/Adiciona-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido:int, Item_pedido_schema:ItemPedidoSchema, session:Session = Depends(pegar_sessao), 
                                usuario: Usuario = Depends(verificar_token)):
      pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
      if not pedido:
            raise HTTPException(status_code=400, detail="Pedido não encontrado!")
      
      if not usuario.admin and usuario.id != pedido.usuario:
            raise HTTPException(status_code=401, detail="Voce não tem autorização para realizar essa operação!")
      itens_pedido = ItensPedidos(Item_pedido_schema.quantidade, Item_pedido_schema.sabor,
                                  Item_pedido_schema.tamanho,
                                  Item_pedido_schema.preco_unitario, id_pedido)

      session.add(itens_pedido)
      pedido.calcular_preco()
      session.commit()
      return {
            "mensagem": "Item adicionado com sucesso!",
            "item_id": itens_pedido.id,
            "preco_pedido": pedido.preco
      }