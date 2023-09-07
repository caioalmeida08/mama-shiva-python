from fastapi import HTTPException
from models.usuario import UsuarioModel
from schemas.usuario import Usuario

from sqlalchemy.orm import Session

import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from pydantic import ValidationError

ACCESS_TOKEN_EXPIRE_MINUTES = 30  
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 
ALGORITHM = "HS256"
JWT_SECRET_KEY = "SENHA_DO_JWT"   
JWT_REFRESH_SECRET_KEY = "EU_SEI_QUE_DEVERIA_ESTAR_NO_ENV"

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def check_token(token: str) -> None:
    try:
        # remove o prefixo "Bearer " do token
        token = token.split(" ")[1]
        
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        print("check_token (usuario.py) - payload: " + str(payload))
        
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code = 401,
                detail="Token expired",
                headers={"Authenticate": "Bearer"},
            )
            
    except(jwt.JWTError, ValidationError):
        print("check_token (usuario.py) - JWTError")
        print("check_token (usuario.py) - ValidationError")
        print("check_token (usuario.py) - token: " + str(token))
        raise HTTPException(
            status_code=400,
            detail="Could not validate credentials",
            headers={"Authenticate": "Bearer"},
        )
        
def get_all_usuario(db: Session):
    print("get_all_usuario")
    return db.query(UsuarioModel).all()

def get_usuario_by_id(db: Session, usuario_id: str):
    print("get_usuario_by_id")
    return db.query(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).first()

def get_usuario_by_email(db: Session, usuario_email: str):
    print("get_usuario_by_email")
    return db.query(UsuarioModel).filter(UsuarioModel.usuario_email == usuario_email).first()

def create_usuario(db: Session, usuario: Usuario):
    print("create_usuario")
    db_usuario = UsuarioModel(**usuario)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: str, usuario: Usuario):
    print("update_usuario")
    db_usuario = db.query(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).first()
    db_usuario.usuario_cpf = usuario.usuario_cpf
    db_usuario.usuario_nome = usuario.usuario_nome
    db_usuario.usuario_email = usuario.usuario_email
    db_usuario.usuario_senha = usuario.usuario_senha
    db_usuario.usuario_telefone = usuario.usuario_telefone
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: str):
    print("delete_usuario")
    db_usuario = db.query(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).first()
    db.delete(db_usuario)
    db.commit()
    return db_usuario
