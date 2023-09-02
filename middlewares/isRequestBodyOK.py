from fastapi import Request, status
from fastapi.responses import JSONResponse
from schemas.mensagem_erro import MensagemErro
from schemas.usuario import UsuarioPartial, Usuario
from pydantic import ValidationError

class IsRequestBodyOK:
    async def __call__(self, request: Request):
        print("IsRequestBodyOK")
        request_method = request.method
        request_route = request.url.path
        request_json = await request.json()
                
        if (request_method == "GET"):
            return 
        
        if (request_route == "/usuario/"):            
            try:
                return UsuarioPartial(**request_json)
            except ValidationError as e:
                request.error = 400
        
        if (request_route == "/usuario/{usuario_id}"):
            try:
                usuario = Usuario(**request_json)
                
            except ValidationError as e:
                request.error = 400
        
        if (request_route == "/usuario/authenticate/"):
            try:
                if (not "usuario_email" in request_json):
                    raise Exception("O campo 'email' é obrigatório")
                
                if (not "usuario_senha" in request_json):
                    raise Exception("O campo 'senha' é obrigatório")
                                
            except Exception as e:
                request.error = 400