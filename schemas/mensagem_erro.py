from fastapi import Request
from http.client import HTTPException
import json

class MensagemErro(HTTPException):
    
    def __init__(self, status_code: int, msg = None):
        self.message = msg
        
        if msg is None:
            if (status_code == 400):
                self.message = "Erro de validacao"
            if (status_code == 401):
                self.message = "Token de acesso invalido ou nao informado"
            if (status_code == 404):
                self.message = "Recurso nao encontrado"

        self.status_code = status_code

        self.json = { "message" : self.message }
    
    