from pydantic import BaseModel
from typing import Optional
 

class UsuarioSchema(BaseModel):
    nome:str
    email:str
    senha:str
    ativo:Optional[bool]
    admin:Optional[bool]

    class Config:
        from_attrubutes = True

class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    nome:str
    senha:str

    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade:int
    sabor:str
    tamanho:str
    preco_unitario:float
    #pedido:int

    class Config:
        from_attributes = True

class ResponsePedidoSchema(BaseModel): # schema para voce personalizar o retorno
    id:int
    status:str
    preco:float

    class Config:
        from_attributes = True