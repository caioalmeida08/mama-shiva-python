from typing import Mapping

from pydantic import BaseModel, Field

from datetime import date, datetime, time, timedelta

# Define o modelo Pydantic para a entrada de informações ao criar um usuário
class ReservaPartial(BaseModel):
    reserva_data: date = Field(...)
    reserva_horario: time = Field(...)
    fk_usuario_id: str = Field(..., max_length=36, min_lenght=36)
    
    class Config:
        from_attributes = True
    
# Define o modelo Pydantic para a saída de informações do usuário
class Reserva(ReservaPartial):
    Reserva_id: str = Field(..., max_length=36, min_length=36, primary_key=True)
    
    
    
    
