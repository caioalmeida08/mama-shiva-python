from models.usuario import UsuarioModel
from schemas.usuario import Usuario

from sqlalchemy.orm import Session

def get_all_usuario(db: Session):
    print("get_all_usuario")
    return db.query(UsuarioModel).all()

def get_usuario_by_id(db: Session, usuario_id: str):
    print("get_usuario_by_id")
    return db.query(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).first()

def create_usuario(db: Session, usuario: Usuario):
    print("create_usuario")
    db_usuario = UsuarioModel(**usuario)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def put_usuario(db: Session, usuario_id: str, usuario: Usuario):
    print("put_usuario")
    db_usuario = db.query(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).first()

    if db_usuario:
        db_usuario.usuario_cpf = usuario.usuario_cpf
        db_usuario.usuario_nome = usuario.usuario_nome
        db_usuario.usuario_email = usuario.usuario_email
        db_usuario.usuario_senha = usuario.usuario_senha
        db_usuario.usuario_telefone = usuario.usuario_telefone
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    return None

def delete_usuario(db: Session, usuario_id: str):
    print("delete_usuario")
    db_usuario = db.query(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).first()
    
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return True
    
    return False 
