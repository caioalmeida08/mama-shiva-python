from fastapi import Request, status
from fastapi.responses import JSONResponse
from schemas.mensagem_erro import MensagemErro

class IsContentTypeApplicationJson:
    async def __call__(self, request: Request):        
        print("IsContentTypeApplicationJson")
        request_method = request.method
        
        request.error = None
        
        content_type = request.headers.get('Content-Type')
        
        if (request_method == "GET"):
            return
        
        if (content_type != "application/json"):
            request.error = 400