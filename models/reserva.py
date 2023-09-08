import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define a classe de modelo do SQLAlchemy para a tabela "reservas"
class ReservaModel(Base):
    __tablename__ = "reservas"
    
    reserva_id = Column('reserva_id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    reserva_data = Column('reserva_data', String(length=11), nullable=False)
    reserva_horario = Column('reserva_horario', String(length=128), nullable=False)
    fk_usuario_id = Column('fk_usuario_id', Text(length=36), nullable=False)