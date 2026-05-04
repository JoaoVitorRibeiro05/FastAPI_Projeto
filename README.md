# 📦 API de Pedidos

API REST desenvolvida com **FastAPI** para gerenciamento de pedidos, com autenticação segura baseada em OAuth2 e JWT.  
A aplicação permite criação, listagem e cancelamento de pedidos, além de controle de acesso via tokens.

---

## 🚀 Funcionalidades

- 🔐 Autenticação com OAuth2 (Password Flow)
- 🔑 Geração de Access Token e Refresh Token
- 🔒 Criptografia de senhas com `bcrypt`
- 📦 Criação de pedidos
- 📄 Listagem de pedidos
- ❌ Cancelamento de pedidos
- 🐳 Containerização com Docker

---

## 🛠️ Tecnologias utilizadas

### Backend
- Python **3.13.7**
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic

### Autenticação & Segurança
- OAuth2 (Password Flow)
- JWT (python-jose)
- passlib + bcrypt
- cryptography

### Banco de Dados
- SQLite

### Infraestrutura
- Docker

---

## 🔐 Autenticação

A API utiliza:

- OAuth2 com fluxo **Password**
- Tokens JWT para autenticação
- Sistema com:
  - **Access Token** (curta duração)
  - **Refresh Token** (renovação de sessão)

As senhas são armazenadas de forma segura utilizando hashing com `bcrypt`.

---

## 🧠 Aprendizados

Durante o desenvolvimento deste projeto, foram aplicados conceitos importantes como:

- Implementação de autenticação com OAuth2
- Uso de JWT para controle de sessão
- Criptografia e segurança de dados sensíveis
- Gerenciamento de migrations com Alembic
- Estruturação de APIs com FastAPI
- Containerização de aplicações com Docker
- Boas práticas de organização de backend

---
```markdown
## 📂 Estrutura do projeto


app/
 ├── models/         # Modelos do banco de dados (SQLAlchemy)
 ├── routers/        # Rotas/endpoints da API
 ├── schemas/        # Schemas (Pydantic)
 ├── dependencies.py # Dependências (auth, db, etc)
 ├── main.py         # Ponto de entrada da aplicação
 └── teste.py        # Testes / scripts auxiliares
