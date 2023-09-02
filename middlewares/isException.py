from fastapi import Request
from fastapi.responses import JSONResponse
from schemas.mensagem_erro import MensagemErro

def isException(request: Request):
    if (request.error): return JSONResponse( status_code= request.error, content= MensagemErro(request.error).json )
