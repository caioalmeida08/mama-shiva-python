from __future__ import annotations

import uuid
import bcrypt
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from schemas.endereco import EnderecoPartial

Base = declarative_base()

# Define a classe de modelo do SQLAlchemy para a tabela "usuarios"
class UsuarioModel(Base):
    __tablename__ = "usuarios"
    
    usuario_id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    usuario_cpf = Column(String, unique=True, index=True)
    usuario_nome = Column(String)
    usuario_email = Column(String, unique=True, index=True)
    usuario_senha = Column(String)
    usuario_telefone = Column(String)
    usuario_endereco = relationship("EnderecoModel", uselist=False)
    
    def __init__(self, usuario_cpf: str, usuario_nome: str, usuario_email: str, usuario_senha: str, usuario_telefone: str, usuario_endereco: EnderecoPartial) -> None:
        self.usuario_cpf = usuario_cpf
        self.usuario_nome = usuario_nome
        self.usuario_email = usuario_email
        self.usuario_senha = bcrypt.hashpw(usuario_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.usuario_telefone = usuario_telefone
        self.usuario_endereco = usuario_endereco
    
    def verify_password(self, senha: str) -> bool:
        return bcrypt.checkpw(senha.encode('utf-8'), self.usuario_senha.encode('utf-8'))
    
class EnderecoModel(Base):
    __tablename__ = "enderecos"

    endereco_id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    endereco_rua = Column(String)
    endereco_numero = Column(String)
    endereco_bairro = Column(String)
    endereco_cidade = Column(String)
    endereco_estado = Column(String)
    fk_usuario_id = Column(String(36), ForeignKey("usuarios.usuario_id"), name="fk_usuario_id")
    
    usuario_relation = relationship("UsuarioModel", back_populates="usuario_endereco")