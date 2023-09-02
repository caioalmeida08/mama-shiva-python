from pydantic import BaseModel

# Define o modelo Pydantic para a entrada de informações ao criar um usuário
class UsuarioPartial(BaseModel):
    usuario_id: str
    usuario_cpf: str
    usuario_nome: str
    usuario_email: str
    usuario_senha: str
    usuario_telefone: str
    
# Define o modelo Pydantic para a saída de informações do usuário
class Usuario(UsuarioPartial):
    usuario_id: int
    
