from sqlalchemy.orm.session import Session
from models.usuario import UsuarioDB
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
