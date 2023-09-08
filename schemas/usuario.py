from typing import Mapping
from pydantic import BaseModel, Field

# Define o modelo Pydantic para a entrada de informações ao criar um usuário
class UsuarioPartial(BaseModel):
    usuario_cpf: str = Field(..., max_length=11, min_length=11)
    usuario_nome: str = Field(..., max_length=128, min_lenght=3)
    usuario_email: str = Field(..., max_length=128, min_lenght=3)
    usuario_senha: str = Field(..., max_length=256, min_lenght=6)
    usuario_telefone: str = Field(..., max_length=11, min_length=10)
    usuario_endereco: str = Field(..., max_length=256, min_length=3)
    
    class Config:
        from_attributes = True
    
# Define o modelo Pydantic para a saída de informações do usuário
class Usuario(UsuarioPartial):
    usuario_id: str = Field(..., max_length=36, min_length=36, primary_key=True)
    
    
    
    
