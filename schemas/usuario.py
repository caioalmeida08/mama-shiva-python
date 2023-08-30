from pydantic import BaseModel

# Define o modelo Pydantic para a saída de informações do usuário
class Usuario(BaseModel):
    id: int
    cpf: str
    nome: str
    email: str
    telefone: str
    
# Define o modelo Pydantic para a entrada de informações ao criar um usuário
class UsuarioPartial(BaseModel):
    cpf: str
    nome: str
    email: str
    senha: str
    telefone: str