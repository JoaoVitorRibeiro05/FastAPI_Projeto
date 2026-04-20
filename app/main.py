from fastapi import FastAPI
from passlib.context import CryptContext # lib para executar a criptografia
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv #lib para variaveis de ambiente
import os

load_dotenv() # carrega as variaveis de ambiente que estao no .env

SECRET_KEY = os.getenv("SECRET_KEY") # pegar minha variaveis no .env
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # transformando em inteiro

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-Form")

from app.routers.auth_routes import auth_router
from app.routers.order_routes import order_router


app.include_router(auth_router) # Incluindo nossas rotas do sistema
app.include_router(order_router)