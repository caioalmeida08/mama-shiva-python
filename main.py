from typing import Mapping

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi import Depends

from sqlalchemy.orm import Session
from database.database import Base



from database.database import SessionLocal, engine

from models.usuario import UsuarioModel
from controllers.usuario import create_usuario, delete_usuario, get_all_usuario, get_usuario_by_id, put_usuario
from schemas.usuario import Usuario

from models.endereco import EnderecoModel
from schemas.endereco import Endereco
from controllers.endereco import create_endereco, delete_endereco, get_all_endereco, get_endereco_by_id, put_endereco

from schemas.mensagem_erro import MensagemErro



from middlewares.isRequestBodyOK import IsRequestBodyOK
from middlewares.isContentTypeApplicationJson import IsContentTypeApplicationJson
from middlewares.isAuth import IsAuth
from middlewares.isException import isException

# Cria uma instância do FastAPI
app = FastAPI()
api_router = APIRouter()

# Cria uma conexão com o banco de dados
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Garante que o usuário esteja autenticado
is_auth = IsAuth()

# Garante que as requisições tenham o cabeçalho Content-Type: application/json
is_content_type_application_json = IsContentTypeApplicationJson()

# Garante que o corpo da requisição seja um objeto do tipo esperado pela rota
is_request_body_ok = IsRequestBodyOK()

@api_router.get("/usuario/")
async def findAllUsuario(request: Request, db: Session = Depends(get_db)):
    if (isException(request)): return isException(request) 
    
    try:
        usuarios = get_all_usuario(db)
        return usuarios
    except Exception as e:
        print("findAllUsuario")
        print(e)
        return JSONResponse(
            status_code= 400,
            content= MensagemErro(400).json
        )

@api_router.post("/usuario/")
async def createUsuario(arg: Mapping[str, str], request: Request, db: Session = Depends(get_db)):
    if (isException(request)): return isException(request) 
    
    try:
        return create_usuario(db, arg)
    except Exception as e:
        print("createUsuario")
        print(e)
        return JSONResponse(
            status_code= 400,
            content= MensagemErro(400).json
        )

@api_router.get("/usuario/{usuario_id}")
async def findUsuarioById(usuario_id: str, request: Request, db: Session = Depends(get_db)):
    if (isException(request)): return isException(request) 
    try:
        usuario = get_usuario_by_id(db, usuario_id)
        return usuario
    except Exception as e:
        print("findUsuarioById")
        print(e)
        return JSONResponse(
            status_code= 400,
            content= MensagemErro(400).json
        )

@api_router.put("/usuario/{usuario_id}")
async def putUsuario(usuario_id: str,usuario_data: Usuario, request: Request,db: Session = Depends(get_db)
):
    if isException(request):
        return isException(request)

    try:
        updated_usuario = put_usuario(db, usuario_id, usuario_data)
        if updated_usuario:
            return updated_usuario  # Retorna os dados atualizados do usuário
        else:
            return JSONResponse(status_code=404, content={"error": "Usuário não encontrado"})
    except Exception as e:
        print("putUsuario")
        print(e)
        return JSONResponse(
            status_code=400,
            content={"error": "Erro ao atualizar usuário"}
        )
    
@api_router.delete("/usuario/{usuario_id}")
async def deleteUsuario(usuario_id: str, request: Request, db: Session = Depends(get_db)):
    if (isException(request)): return isException(request) 
    
    try:
        return delete_usuario(db, usuario_id)
    except Exception as e:
        print("deleteUsuario")
        print(e)
        return JSONResponse(
            status_code= 400,
            content= MensagemErro(400).json
        )
    
@api_router.post("/endereco/")
async def createEndereco(arg: Mapping[str, str], request: Request, db: Session = Depends(get_db)):
    if (isException(request)): return isException(request) 
    
    try:
        return create_endereco(db, arg)
    except Exception as e:
        print("createEndereco")
        print(e)
        return JSONResponse(
            status_code= 400,
            content= MensagemErro(400).json
        )
    


    


# Liga os middlewares. Manter sempre após o fim das rotas.
# Não alterar a ordem dos middlewares.
app.include_router(api_router, dependencies=[
    Depends(is_auth),
    Depends(is_content_type_application_json),
    Depends(is_request_body_ok),
    ]
    )