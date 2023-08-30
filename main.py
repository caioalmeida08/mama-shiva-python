from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from models.usuario import Usuario
from schemas.usuario import UsuarioPartial, Usuario

from middlewares.isContentTypeApplicationJson import IsContentTypeApplicationJson
from starlette.middleware.base import BaseHTTPMiddleware

# Cria uma instância do FastAPI
app = FastAPI()

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

is_content_type_application_json = IsContentTypeApplicationJson()
app.add_middleware(BaseHTTPMiddleware, dispatch=is_content_type_application_json)

# Define a rota POST para criar um usuário
@app.post("/usuario/", response_model= UsuarioPartial)
def criar_usuario(usuario: Usuario):
    return {"ok": "ok"}
    
    

# Define a rota GET para ler informações de um usuário pelo ID
@app.get("/usuarios/{usuario_id}", response_model=UsuarioPartial)
def ler_usuario(usuario_id: int):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario
