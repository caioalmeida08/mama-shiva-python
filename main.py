from typing import Mapping
from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi import Depends
from middlewares.isAuth import IsAuth
from schemas.mensagem_erro import MensagemErro

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from models.usuario import Usuario
from schemas.usuario import UsuarioPartial, Usuario

from starlette.middleware.base import BaseHTTPMiddleware
from middlewares.isRequestBodyOK import IsRequestBodyOK
from middlewares.isContentTypeApplicationJson import IsContentTypeApplicationJson

# Cria uma instância do FastAPI
app = FastAPI()
api_router = APIRouter()

# URL de conexão com o banco de dados SQLite
DATABASE_URL = "sqlite:///./teste.db"

# Cria uma conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe base declarativa para definir modelos do SQLAlchemy
Base = declarative_base()

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Garante que as requisições tenham o cabeçalho Content-Type: application/json
is_content_type_application_json = IsContentTypeApplicationJson()

# Garante que o corpo da requisição seja um objeto do tipo esperado pela rota
is_request_body_ok = IsRequestBodyOK()

# Garante que o usuário esteja autenticado
is_auth = IsAuth()

# Define a rota POST para criar um usuário
@api_router.post("/usuario/")
async def criar_usuario(arg: Mapping[str, str], request: Request):
    if (request.error): return JSONResponse( status_code= request.error, content= MensagemErro(request.error).json )
    
    return JSONResponse(
        status_code= 200,
        content= arg
    )
    
# Define a rota POST para criar um usuário
@api_router.delete("/usuario/")
async def criar_usuario(arg: Mapping[str, str], request: Request):
    if (request.error): return JSONResponse( status_code= request.error, content= MensagemErro(request.error).json )
    
    return JSONResponse(
        status_code= 200,
        content= arg
    )
    
@api_router.get("/usuarios/{usuario_id}")
def ler_usuario(usuario_id: int):
    print("ler usuario")
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario

# Liga os middlewares. Manter sempre após o fim das rotas.
app.include_router(api_router, dependencies=[
    Depends(is_auth),
    Depends(is_content_type_application_json),
    Depends(is_request_body_ok)]
    )