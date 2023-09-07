from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from database.database import Base
import uuid

class EnderecoModel(Base):
    __tablename__ = "enderecos"

    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    endereco_rua = Column(String)
    endereco_numero = Column(String)
    endereco_bairro = Column(String)
    endereco_cidade = Column(String)
    endereco_estado = Column(String)
    fk_usuario_id = Column(String(36), ForeignKey("usuarios.id"))