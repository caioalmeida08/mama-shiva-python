from pydantic import BaseModel

# Define o modelo Pydantic para a saída de informações do usuário
class Usuario(BaseModel):
    usuario_id: int
    usuario_cpf: str
    usuario_nome: str
    usuario_email: str
    usuario_telefone: str
    
# Define o modelo Pydantic para a entrada de informações ao criar um usuário
class UsuarioPartial(BaseModel):
    usuario_cpf: str
    usuario_nome: str
    usuario_email: str
    usuario_senha: str
    usuario_telefone: str