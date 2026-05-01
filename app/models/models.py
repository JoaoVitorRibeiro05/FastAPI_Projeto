from sqlalchemy import create_engine,Column,String,Integer,Boolean,Float,ForeignKey # criar nosso banco de dados, que no caso será o sqlite
from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy_utils.types import ChoiceType




# cria a conexao do banco
db = create_engine("sqlite:///database.db")

# cria a base do banco
base = declarative_base()

# criar as classes/tabelas do banco
class Usuario(base):
    __tablename__ = "usuarios" # nome da minha tabela

    id = Column("id", Integer, primary_key=True, autoincrement=True) # passa como parametros o nome da coluna(id) e o tipo de dados da coluna, nullable= False = campo nao pode ser nulo
    nome = Column("nome", String,nullable= False) # nullable= False = campo nao pode ser nulo
    email = Column("email", String,nullable= False)
    isativo = Column("isativo", Boolean)
    senha = Column("senha",String,nullable= False)
    admin = Column("admin", Boolean,default= False) 

    def __init__(self,nome,email,senha,isativo=True,admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.isativo = isativo
        self.admin = admin

class Pedido(base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDOS =(
    #     ("PENDENTE","PENDENTE"),
    #     ("CANCELADO","CANCELADO"),
    #     ("FINALIZADO","FINALIZADO")
        
    # )

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    status = Column("status", String) # status pendente, cancelado e finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id"))# chave estrangeira da tabela usuarios
    preco = Column("preco",Float)
    itens = relationship("ItensPedidos", cascade="all,delete")

    def __init__(self,usuario,status="PENDENTE",preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco 
    
    def calcular_preco(self):
        
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)



class ItensPedidos(base):
    __tablename__ = "itens_pedidos"

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    quantidade = Column("quantidade",Integer)
    sabor = Column("sabor",String)
    tamanho = Column("tamanho",String)
    preco_unitario = Column("preco_unitario", Integer)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self,quantidade,sabor,tamanho,preco_unitario,pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

# executa a criacao dos metadados do seu banco (cria efetivamente o banco de dados) com alembic
# primeiramente ao instalar o alembic, execute o comando alembic init alembic(cria as pastas do alembic e inicializa)
# comando -> alembic revision --autogenerate -m "initial migration" 
# comando para atualizar o esquema do banco de dados  -> alembic upgrade head
# ou seja, sempre que eu alterar alguma tabela no meu banco de dados, eu tenho que fazer o processo de migration e depois eu tenho que fazer o comando de upgrade(alembic upgrade head)



#instalar alembic
#configurar o env.py -  importar(import sys import os), adicionar esse comando sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
