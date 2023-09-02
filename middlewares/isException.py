from fastapi import Request
from fastapi.responses import JSONResponse
from schemas.mensagem_erro import MensagemErro

def isException(request: Request):
    print("isException")
    if (request.error_instance): print(request.error_instance)
    if (request.error): return JSONResponse( status_code= request.error, content= MensagemErro(request.error).json )
