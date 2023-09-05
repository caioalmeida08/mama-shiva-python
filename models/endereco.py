from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.usuario import UsuarioModel

Base = declarative_base()

class EnderecoModel(Base):
    __tablename__ = "enderecos"

    endereco_id = Column('endereco_id', Integer, primary_key=True)
    endereco_rua = Column(String)
    endereco_numero = Column(Integer)
    endereco_bairro = Column(String)
    endereco_cidade = Column(String)
    endereco_estado = Column(String)
    fk_usuario_id = Column(Text(length=36), ForeignKey('usuarios.usuario_id'))
    usuario = relationship(UsuarioModel, back_populates="enderecos")