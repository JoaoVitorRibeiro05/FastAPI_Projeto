from fastapi import FastAPI
from passlib.context import CryptContext # lib para executar a criptografia
from dotenv import load_dotenv #lib para variaveis de ambiente
import os

load_dotenv() # carrega as variaveis de ambiente que estao no .env

SECRET_KEY = os.getenv("SECRET_KEY") # pegar minha variaveis no .env

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

from app.routers.auth_routes import auth_router
from app.routers.order_routes import order_router


app.include_router(auth_router) # Incluindo nossas rotas do sistema
app.include_router(order_router)