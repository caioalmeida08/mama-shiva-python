from main import SessionLocal
from models.usuario import Usuario
from schemas.mensagem_erro import MensagemErro

def create_usuario(usuario: Usuario, SessionLocal: SessionLocal):
    db = SessionLocal()
    
    try:
        db_usuario = Usuario(**usuario.dict())
    except :
        print("erro aqui")
        raise MensagemErro(400)
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario