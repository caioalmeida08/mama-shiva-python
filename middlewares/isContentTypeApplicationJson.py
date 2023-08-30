from fastapi import Request, status
from fastapi.responses import JSONResponse
from schemas.mensagem_erro import MensagemErro

class IsContentTypeApplicationJson:
    async def __call__(self, request: Request, call_next):
        content_type = request.headers.get('Content-Type')
        
        if (content_type != "application/json"):
            response_status = 400
            return JSONResponse(status_code=response_status, content= MensagemErro(response_status).json )
        
        print(content_type)
        
        response = await call_next(request)
        
        return response