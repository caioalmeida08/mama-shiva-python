from sqlalchemy.orm.session import Session
from models.usuario import Usuarios as UsuarioDB
from schemas.usuario import UsuarioPartial
from schemas.mensagem_erro import MensagemErro

def create_usuario(usuario: UsuarioPartial, SessionLocal: Session):
    db = SessionLocal()
    try:
        db_usuario = UsuarioDB(**usuario.dict())
    except:
        print("Erro:")
        raise MensagemErro(400)
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def read_usuario(usuario_id: int, SessionLocal: Session):
    db = SessionLocal()
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    
    if not usuario:
        raise MensagemErro(404)
    
    return usuario

def put_usuario(usuario_id: int, usuario: UsuarioPartial, SessionLocal: Session):
    db = SessionLocal()
    db_usuario = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    
    if not db_usuario:
        raise MensagemErro(404)
    
    db_usuario.cpf = usuario.cpf
    db_usuario.nome = usuario.nome
    db_usuario.email = usuario.email
    db_usuario.senha = usuario.senha
    db_usuario.telefone = usuario.telefone
    
    db.commit()
    db.refresh(db_usuario)
    
    return db_usuario

def delete_usuario (usuario_id: int, SessionLocal: Session):
    db = SessionLocal()
    db_usuario = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    
    if not db_usuario:
        raise MensagemErro(404)
    
    db.delete(db_usuario)
    db.commit()
    
    return db_usuario