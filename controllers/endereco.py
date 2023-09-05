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