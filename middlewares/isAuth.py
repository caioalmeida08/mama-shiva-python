from fastapi import Request, status
from fastapi.responses import JSONResponse

# Lista de rotas que não necessitam de autenticação
rotas_sem_autenticacao = [
    { "method": "DELETE", "route": "/usuario/bda4bf96-c95c-40ab-b5d9-6ef854a0489a" },
    { "method": "PUT", "route": "/usuario/bda4bf96-c95c-40ab-b5d9-6ef854a0489a" },
    { "method": "GET", "route": "/usuario/" },
    { "method": "POST", "route": "/usuario/" },
    { "method": "POST", "route": "/usuario/authenticate" },
]

class IsAuth:
    async def __call__(self, request: Request): 
        print("IsAuth")  
        
        request_method_route = { "method": request.method, "route": request.url.path }
        print(request.url)
        
        request.error = None
        request.error_instance = None

        return
        
        # Ignora rotas que não necessitam de autenticação
        if (request_method_route in rotas_sem_autenticacao):
            return
        
        request_cookies = request.cookies

        if (not "Authenticate" in request_cookies):
            request.error = 401
            request.error_instance = Exception("Usuário não autenticado")
            return