from fastapi import APIRouter,Depends,HTTPException
from app.models.models import Usuario,db
from app.dependecies import pegar_sessao
from app.main import bcrypt_context
from app.schemas.schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix= "/auth",tags = ["auth"])

@auth_router.get("/")
async def home():
    """Rota padrao de autenticacao"""
    return {
        "mensagem":"voce acessou a rota de autenticacao",
        "Autenticacao": True
            }

@auth_router.post("/criar_conta",summary="Criar conta do usuário")
async def criar_conta(usuario_schema: UsuarioSchema ,session: Session = Depends(pegar_sessao)): # padronizacao de entradas de dados usando schemas


    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        # ja existe um usuário com esse email
        raise HTTPException(status_code=400,detail="Email já cadastrado!")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha) #criptografando a senha que o usuário passou no parametro
        novo_usuario = Usuario(usuario_schema.nome,usuario_schema.email,senha_criptografada,usuario_schema.ativo,usuario_schema.admin)
        session.add(novo_usuario) # adiciona um novo usuário
        session.commit()
        raise HTTPException(status_code=200, detail="Usuário cadastrado com sucesso! ")
