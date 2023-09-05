from models.endereco import EnderecoModel
from schemas.endereco import Endereco

from sqlalchemy.orm import Session

def get_all_endereco(db: Session):
    print("get_all_endereco")
    return db.query(EnderecoModel).all()

def get_endereco_by_id(db: Session, endereco_id: str):
    print("get_endereco_by_id")
    return db.query(EnderecoModel).filter(EnderecoModel.endereco_id == endereco_id).first()

def create_endereco(db: Session, endereco: Endereco):
    print("create_endereco")
    db_endereco = EnderecoModel(**endereco)
    db.add(db_endereco)
    db.commit()
    db.refresh(db_endereco)
    return db_endereco

def put_endereco(db: Session, endereco_id: str, endereco: Endereco):
    print("put_endereco")
    db_endereco = db.query(EnderecoModel).filter(EnderecoModel.endereco_id == endereco_id).first()

    if db_endereco:
        db_endereco.endereco_rua = endereco.endereco_rua
        db_endereco.endereco_numero = endereco.endereco_numero
        db_endereco.endereco_bairro = endereco.endereco_bairro
        db_endereco.endereco_cidade = endereco.endereco_cidade
        db_endereco.endereco_estado = endereco.endereco_estado
        db.commit()
        db.refresh(db_endereco)
        return db_endereco
    
    return None

def delete_endereco(db: Session, endereco_id: str):
    print("delete_endereco")
    db_endereco = db.query(EnderecoModel).filter(EnderecoModel.endereco_id == endereco_id).first()
    
    if db_endereco:
        db.delete(db_endereco)
        db.commit()
        return True
    
    return False