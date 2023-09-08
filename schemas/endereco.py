from pydantic import BaseModel, Field
import uuid

# Define o modelo Pydantic para a entrada de informações ao criar um endereço
class EnderecoPartial(BaseModel):
    endereco_rua: str = Field(..., max_length=128, min_length=3)
    endereco_numero: int = Field(..., gt=0)
    endereco_bairro: str = Field(..., max_length=32, min_length=3)
    endereco_cidade: str = Field(..., max_length=64, min_length=3)
    endereco_estado: str = Field(..., max_length=64, min_length=2)
    
    class Config:
        from_attributes = True
        
# Define o modelo Pydantic para a saída de informações do endereço
class Endereco(EnderecoPartial):
    endereco_id: str = Field(..., max_length=36, min_length=36, primary_key=True)
    fk_usuario_id: str = Field(..., max_length=36, min_length=36) 
    