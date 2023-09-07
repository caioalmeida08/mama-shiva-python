from fastapi import Request

from controllers.usuario import check_token

class Rota:
    def __init__(self, metodo: str, path: str) -> None:
        self.metodo = metodo
        self.path = path
        
    def __eq__(self, other):
        return self.metodo == other.metodo and self.path == other.path
    
rotasSemAutenticacao = [
    Rota("POST", "/usuario/authenticate/"),
    Rota("POST", "/usuario/"),
    # Rota("GET", "/usuario/"),
]

async def isAuth(request: Request) -> bool:
    print("isAuth (isAuth.py) - START")
    
    rota_atual = Rota(request.method, request.url.path)
    
    if (rota_atual in rotasSemAutenticacao):
        print("isAuth (isAuth.py) - OK (SEM AUTENTICAÇÃO)")
        return True
    
    if (not request.headers.get("Authorization")):
        print("isAuth (isAuth.py) - NOT OK (AUTHORIZATION NOT PROVIDED)")
        return False
    
    print("isAuth (isAuth.py) - (STARTING CHECK)")
    check_token(request.headers.get("Authorization"))
    
    
    return True