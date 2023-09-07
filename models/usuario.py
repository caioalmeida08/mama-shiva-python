from sqlalchemy import Column, Integer, String
from database.database import Base 
import uuid

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    usuario_cpf = Column(String, unique=True, index=True)
    usuario_nome = Column(String)
    usuario_email = Column(String, unique=True, index=True)
    usuario_senha = Column(String)
    usuario_telefone = Column(String)