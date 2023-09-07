import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    usuario_id = Column('usuario_id', Text(length=36), primary_key=True, default=str(uuid.uuid4()))
    usuario_cpf = Column(String(11))
    usuario_nome = Column(String(128))
    usuario_email = Column(String(128))
    usuario_senha = Column(String(256))
    usuario_telefone = Column(String(11))
    enderecos = relationship("EnderecoModel", back_populates="usuario")