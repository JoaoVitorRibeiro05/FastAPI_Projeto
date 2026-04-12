from fastapi import APIRouter


auth_router = APIRouter(prefix= "/auth",tags = ["auth"])

@auth_router.get("/")
async def autenticar():
    """Rota padrao de autenticacao"""
    return {
        "mensagem":"voce acessou a rota de autenticacao",
        "Autenticacao": False
            }

@auth_router.put("/altera_usuario")
def Alterar_user():
    return {"mensagem": "digite o id do usuario para realizar a alteracao"}

@auth_router.delete("/deletar_usuario")
def Deletar_user():
    return {
        "Autenticacao": True,
        "Mensagem": "Digite o id para deletar usuario"
            }