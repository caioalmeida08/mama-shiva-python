import uuid
from sqlalchemy import Column, String, Text, ForeignKey,SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define a classe de modelo do SQLAlchemy para a tabela "enderecos"
class EnderecoModel(Base):
    __tablename__="enderecos"

    endereco_id = Column('endereco_id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    endereco_rua = Column(String)
    endereco_numero = Column(SmallInteger)
    endereco_bairro = Column(String)
    endereco_cidade = Column(String)
    endereco_estado = Column(String)
    fk_usuario_id = Column('fk_usuario_id', Text(length=36), ForeignKey('usuarios.usuario_id'))