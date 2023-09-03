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
