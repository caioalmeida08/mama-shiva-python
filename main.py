from typing import Annotated, Mapping
from uuid import uuid4

from fastapi import FastAPI, APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from database.database import SessionLocal, engine

from controllers.usuario import create_usuario, get_all_usuario, get_usuario_by_email, create_access_token, create_refresh_token

from models.usuario import UsuarioModel

from schemas.usuario import Usuario, UsuarioPartial
from schemas.mensagem_erro import MensagemErro

from middlewares.isContentTypeApplicationJson import isContentTypeApplicationJson
from middlewares.isRequestBodyOK import isRequestBodyOK
from middlewares.isAuth import isAuth


# Cria uma instância do FastAPI
app = FastAPI()

# Habilita ou desabilita o modo de debug
app.state.debug = True

# Middlewares
async def middlewares(request: Request):
    isContentTypeApplicationJsonMiddleware = isContentTypeApplicationJson(request)
    print("middlewares (main.py) - isContentTypeApplicationJsonMiddleware: " + str(isContentTypeApplicationJsonMiddleware))
    
    if (not isContentTypeApplicationJsonMiddleware):
        if (request.app.state.debug):
            raise HTTPException(status_code=400, detail="Content-Type inválido. Valor recebido: " + str(request.headers.get("Content-Type")))
        else:
            raise HTTPException(status_code=400, detail=MensagemErro(400).message)
        
    isRequestBodyOKMiddleware = await isRequestBodyOK(request)
    print("middlewares (main.py) - isRequestBodyOKMiddleware: " + str(isRequestBodyOKMiddleware))
    
    if (not isRequestBodyOKMiddleware):
        if (request.app.state.debug):
            raise HTTPException(status_code=400, detail="Body inválido. Valor recebido: " + str(await request.body()))
        else:
            raise HTTPException(status_code=400, detail=MensagemErro(400).message)
        
    isAuthMiddleware = await isAuth(request)
    print("middlewares (main.py) - isAuthMiddleware: " + str(isAuthMiddleware))
    
    if (not isAuthMiddleware):
        if (request.app.state.debug):
            raise HTTPException(status_code=401, detail="Não autorizado")
        else:
            raise HTTPException(status_code=401, detail=MensagemErro(401).message)
    
# Cria uma conexão com o banco de dados
UsuarioModel.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/usuario/")
async def findAllUsuario(request: Request, response: Response, middleware: Mapping = Depends(middlewares), db: Session = Depends(get_db)):
    try:
        usuarios = get_all_usuario(db)
        for usuario in usuarios:
            usuario.usuario_senha = None
            
        return usuarios 
    except Exception as e:
        if(request.app.state.debug):
            raise HTTPException(status_code=400, detail=str(e))
        
        raise HTTPException(status_code=400, detail=MensagemErro(400).message)

@app.post("/usuario/")
async def createUsuario(request: Request, response: Response, middleware: Mapping = Depends(middlewares), db: Session = Depends(get_db)):
    try:
        request_json = await request.json()
        
        usuarioPartial = UsuarioPartial(**request_json)

        usuario = UsuarioModel(
            usuario_cpf=usuarioPartial.usuario_cpf,
            usuario_nome=usuarioPartial.usuario_nome,
            usuario_email=usuarioPartial.usuario_email,
            usuario_senha=usuarioPartial.usuario_senha,
            usuario_telefone=usuarioPartial.usuario_telefone
        )
        
        usuarioDb = create_usuario(db, usuario)
        usuarioDb.usuario_senha = None
        return usuarioDb
        
    except Exception as e:
        if(request.app.state.debug):
            raise HTTPException(status_code=400, detail=str(e))
        
        raise HTTPException(status_code=400, detail=MensagemErro(400).message)

@app.post("/usuario/authenticate/")
async def authenticateUsuario(request: Request, response: Response, middleware: Mapping = Depends(middlewares), db: Session = Depends(get_db)):
    try:
        request_json = await request.json()
        request_email = request_json.get("usuario_email")
        request_senha = request_json.get("usuario_senha")
        
        if (not request_email):
            raise Exception("O campo 'usuario_email' é obrigatório")
        
        if (not request_senha):
            raise Exception("O campo 'usuario_senha' é obrigatório")
        
        usuarioDB = get_usuario_by_email(db, request_email)
        
        if (not usuarioDB):
            if(request.app.state.debug):
                raise Exception("Usuário não encontrado")
            
            raise Exception(MensagemErro(404).message)
        
        isRightPassword = usuarioDB.verify_password(request_senha)
        
        if (not isRightPassword):
            if(request.app.state.debug):
                raise Exception("Senha incorreta")
            
            raise Exception(MensagemErro(401).message)
        
        response.headers["Authorization"] = "Bearer " + create_access_token(usuarioDB.usuario_id)
        response.headers["Refresh-Token"] = create_refresh_token(usuarioDB.usuario_id)
        
    except Exception as e:
        if(request.app.state.debug):
            raise HTTPException(status_code=404, detail=str(e))
        
        raise HTTPException(status_code=404, detail=MensagemErro(404).message)
    
    return {
        "usuario_id": usuarioDB.usuario_id,
        "usuario_nome": usuarioDB.usuario_nome,
        "usuario_email": usuarioDB.usuario_email,
        "usuario_telefone": usuarioDB.usuario_telefone
    }