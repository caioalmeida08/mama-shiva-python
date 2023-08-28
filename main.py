from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

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

# Define a classe de modelo do SQLAlchemy para a tabela "usuarios"
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, unique=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    telefone = Column(String)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Define o modelo Pydantic para a saída de informações do usuário
class UsuarioOut(BaseModel):
    id: int
    cpf: str
    nome: str
    email: str
    telefone: str

# Define o modelo Pydantic para a entrada de informações ao criar um usuário
class UsuarioCreate(BaseModel):
    cpf: str
    nome: str
    email: str
    senha: str
    telefone: str

# Define a rota POST para criar um usuário
@app.post("/usuarios/", response_model=UsuarioOut)
def criar_usuario(usuario: UsuarioCreate):
    db = SessionLocal()
    db_usuario = Usuario(**usuario.dict())  # Cria um objeto Usuario a partir dos dados do modelo Pydantic
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Define a rota GET para ler informações de um usuário pelo ID
@app.get("/usuarios/{usuario_id}", response_model=UsuarioOut)
def ler_usuario(usuario_id: int):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario