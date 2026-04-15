from app.models.models import db
from sqlalchemy.orm import sessionmaker



def pegar_sessao():
     try:
        Session = sessionmaker(bind=db) # passar a conexao do banco de dados que criamos no models
        session = Session() # abrindo sessao
        yield session
     finally: # independente se der erro ou nao irá executar, e fechar a conexao
        session.close()
