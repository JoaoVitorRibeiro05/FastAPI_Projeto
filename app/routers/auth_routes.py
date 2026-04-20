from fastapi import APIRouter,Depends,HTTPException
from app.models.models import Usuario,db
from app.dependecies import pegar_sessao,verificar_token
from app.main import bcrypt_context,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,SECRET_KEY
from app.schemas.schemas import UsuarioSchema
from sqlalchemy.orm import Session
from app.schemas.schemas import LoginSchema
from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix= "/auth",tags = ["auth"])


def criar_token(id_usuario,duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)): # utilizando jwt e hs256
    data_expiracao = datetime.now(timezone.utc) + duracao_token # data de expiracao do token, que seria a hora atual + tempo que definimos que expira o access_token(30 min)
    dict_info = {
        "sub" : str(id_usuario),
        "exp" : int(data_expiracao.timestamp())
    }
    jwt_codificado = jwt.encode(dict_info,SECRET_KEY,ALGORITHM)
    return jwt_codificado



def autenticar_usuario(nome,senha,session):
    usuario = session.query(Usuario).filter(Usuario.nome==nome).first()
    

    if not usuario:
        return False
    elif not bcrypt_context.verify(senha,usuario.senha):
        return False

    return usuario

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
        novo_usuario = Usuario(
            usuario_schema.nome,
            usuario_schema.email,
            senha_criptografada,
            usuario_schema.ativo,
            usuario_schema.admin
            )
        session.add(novo_usuario) # adiciona um novo usuário
        session.commit()
        raise HTTPException(status_code=200, detail="Usuário cadastrado com sucesso! ")
 
    
@auth_router.post("/login",summary="Login")
async def login(login_schema:LoginSchema,session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.nome,login_schema.senha,session)
    if not usuario:
        raise HTTPException(status_code = 400, detail="Usuário não encontrado ou credenciais inválidas")
    
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id,duracao_token=timedelta(days=7))
        return {
            "mensagem": "Usuário logado no sistema!",
            "access_token": access_token,
            "refresh_token" : refresh_token,
            "token_type": "bearer"
        }

@auth_router.post("/login-Form",summary="Login-Form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(),session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username,dados_formulario.password,session)
    if not usuario:
        raise HTTPException(status_code = 400, detail="Usuário não encontrado ou credenciais inválidas")
    
    else:
        access_token = criar_token(usuario.id)
        #refresh_token = criar_token(usuario.id,duracao_token=timedelta(days=7))
        return {
            "mensagem": "Usuário logado no sistema!",
            "access_token": access_token,
            "token_type": "bearer"
        }

@auth_router.get("/refresh",summary="Refresh-Token")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    #verificar token
    access_token = criar_token(usuario.id)
    
    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }

