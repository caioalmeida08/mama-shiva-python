from typing import Annotated, Mapping
from uuid import uuid4

from fastapi import FastAPI, APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from controllers.reserva import create_reserva, delete_reserva, get_all_reserva, get_reserva_by_id, update_reserva

from database.database import SessionLocal, engine

from controllers.usuario import create_usuario, delete_usuario, get_all_usuario, get_usuario_by_email,get_usuario_by_id, create_access_token, create_refresh_token, update_usuario
from models.reserva import ReservaModel

from models.usuario import UsuarioModel
from schemas.reserva import ReservaPartial

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
            raise HTTPException(status_code=401, detail="O token de autenticação é inválido")
        else:
            raise HTTPException(status_code=401, detail=MensagemErro(401).message)
    
# Cria uma conexão com o banco de dados
UsuarioModel.metadata.create_all(bind=engine)
ReservaModel.metadata.create_all(bind=engine)

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
        
        usuarioDb = create_usuario(db, usuarioPartial.dict())
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

@app.get("/usuario/{usuario_id}")
async def findUsuarioById(request: Request, response: Response, middleware: Mapping = Depends(middlewares), usuario_id: str = None, db: Session = Depends(get_db)):
    try:
        usuario = get_usuario_by_id(db, usuario_id)
        usuario.usuario_senha = None
        return usuario
    except Exception as e:
        if(request.app.state.debug):
            raise HTTPException(status_code=404, detail=str(e))
        
        raise HTTPException(status_code=404, detail=MensagemErro(404).message)
    
@app.put("/usuario/{usuario_id}")
async def updateUsuario(request: Request, response: Response, middleware: Mapping = Depends(middlewares), usuario_id: str = None, db: Session = Depends(get_db)):
    try:
        request_json = await request.json()
        
        usuarioPartial = UsuarioPartial(**request_json)
        
        usuarioDb = update_usuario(db, usuario_id, usuarioPartial.dict())
        usuarioDb.usuario_senha = None
        
        return usuarioDb
    except Exception as e:
        if(request.app.state.debug):
            raise HTTPException(status_code=404, detail=str(e))
        
        raise HTTPException(status_code=404, detail=MensagemErro(404).message)
    
@app.delete("/usuario/{usuario_id}")
async def deleteUsuario(request: Request, response: Response, middleware: Mapping = Depends(middlewares), usuario_id: str = None, db: Session = Depends(get_db)):
    try:
        usuarioDb = delete_usuario(db, usuario_id)
        usuarioDb.usuario_senha = None
        return usuarioDb
    except Exception as e:
        if(request.app.state.debug):
            raise HTTPException(status_code=404, detail=str(e))
        
        raise HTTPException(status_code=404, detail=MensagemErro(404).message)

@app.get("/reserva/")
async def findAllReserva(request: Request, response: Response, middleware: Mapping = Depends(middlewares), db: Session = Depends(get_db)):
    try:
        reservas = get_all_reserva(db)
        return reservas
    except Exception as e:
        if(request.app.state.debug):
            raise HTTPException(status_code=400, detail=str(e))
        
        raise HTTPException(status_code=400, detail=MensagemErro(400).message)
    
@app.post("/reserva/")
async def createReserva(request: Request, response: Response, middleware: Mapping = Depends(middlewares), db: Session = Depends(get_db)):
    try:
        request_json = await request.json()
        
        reserva_horario_allowed_values = [
            "07:00",
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00"
        ]
        
        if (not request_json.get("reserva_horario") in reserva_horario_allowed_values):
            raise Exception("O campo 'reserva_horario' deve ser um dos seguintes valores: " + str(reserva_horario_allowed_values))
        
        isUsuarioDb = get_usuario_by_id(db, request_json.get("fk_usuario_id"))
        
        if (not isUsuarioDb):
            raise Exception("O usuário informado não existe")
        
        reservaPartial = ReservaPartial(**request_json)
        
        reservaDb = create_reserva(db, reservaPartial.dict())
        return reservaDb
    except Exception as e:
        if(request.app.state.debug):
            raise HTTPException(status_code=400, detail=str(e))
        
        raise HTTPException(status_code=400, detail=MensagemErro(400).message)
    
@app.put("/reserva/{reserva_id}")
async def updateReserva(request: Request, response: Response, middleware: Mapping = Depends(middlewares), reserva_id: str = None, db: Session = Depends(get_db)):
    try:
        request_json = await request.json()
        
        reserva_horario_allowed_values = [
            "07:00",
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00"
        ]
        
        if (not request_json.get("reserva_horario") in reserva_horario_allowed_values):
            raise Exception("O campo 'reserva_horario' deve ser um dos seguintes valores: " + str(reserva_horario_allowed_values))
        
        isUsuarioDb = get_usuario_by_id(db, request_json.get("fk_usuario_id"))
        
        if (not isUsuarioDb):
            raise Exception("O usuário informado não existe")
        
        reservaPartial = ReservaPartial(**request_json)
        
        reservaDb = update_reserva(db, reserva_id, reservaPartial.dict())
        return reservaDb
    
    except Exception as e:
        if(request.app.state.debug):
            raise HTTPException(status_code=400, detail=str(e))
        
        raise HTTPException(status_code=400, detail=MensagemErro(400).message)
    
@app.delete("/reserva/{reserva_id}")
async def deleteReserva(request: Request, response: Response, middleware: Mapping = Depends(middlewares), reserva_id: str = None, db: Session = Depends(get_db)):
    try:
        reservaDb = delete_reserva(db, reserva_id)
        return reservaDb
    except Exception as e:
        if(request.app.state.debug):
            raise HTTPException(status_code=404, detail=str(e))
        
        raise HTTPException(status_code=404, detail=MensagemErro(404).message)