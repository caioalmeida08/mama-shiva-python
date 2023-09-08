import uuid
import bcrypt
from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define a classe de modelo do SQLAlchemy para a tabela "usuarios"
class UsuarioModel(Base):
    __tablename__ = "usuarios"
    
    usuario_id = Column('usuario_id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    usuario_cpf = Column(String, unique=True, index=True)
    usuario_nome = Column(String)
    usuario_email = Column(String, unique=True, index=True)
    usuario_senha = Column(String)
    usuario_telefone = Column(String)
    usuario_endereco = Column(String)
    
    def __init__(self, usuario_cpf: str, usuario_nome: str, usuario_email: str, usuario_senha: str, usuario_telefone: str, usuario_endereco) -> None:
        self.usuario_cpf = usuario_cpf
        self.usuario_nome = usuario_nome
        self.usuario_email = usuario_email
        self.usuario_senha = bcrypt.hashpw(usuario_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.usuario_telefone = usuario_telefone
        self.usuario_endereco = usuario_endereco
    
    def verify_password(self, senha: str) -> bool:
        return bcrypt.checkpw(senha.encode('utf-8'), self.usuario_senha.encode('utf-8'))