from fastapi import Request, status
from fastapi.responses import JSONResponse
from schemas.mensagem_erro import MensagemErro

class IsContentTypeApplicationJson:
    async def __call__(self, request: Request):        
        print("IsContentTypeApplicationJson")
        request_method = request.method
        
        # Ignora rotas GET
        if (request_method == "GET"):
            return
        
        content_type = request.headers.get('Content-Type')
        
        if (content_type != "application/json"):
            request.error = 400
            request.error_instance = Exception("O cabeçalho 'Content-Type' deve ser 'application/json'")