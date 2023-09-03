from fastapi import Request
from schemas.usuario import UsuarioPartial, Usuario
from pydantic import ValidationError

class IsRequestBodyOK:
    async def __call__(self, request: Request):
        print("IsRequestBodyOK")
        
        # Ignora rotas GET
        if (request.method == "GET"):
            return 
        
        request_route = request.url.path
        request_json = await request.json()
        
        if (request_route == "/usuario/"):            
            try:
                return UsuarioPartial(**request_json)
            except ValidationError as e:
                request.error = 400
                request.error_instance = e
        
        if (request_route == "/usuario/{usuario_id}"):
            try:
                return Usuario(**request_json)
            except ValidationError as e:
                request.error = 400
                request.error_instance = e
        
        if (request_route == "/usuario/authenticate/"):
            try:
                if (not "usuario_email" in request_json):
                    raise Exception("O campo 'email' é obrigatório")
                
                if (not "usuario_senha" in request_json):
                    raise Exception("O campo 'senha' é obrigatório")
                                
            except Exception as e:
                request.error = 400
                request.error_instance = e