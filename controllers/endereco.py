from fastapi import HTTPException
from models.usuario import EnderecoModel

from sqlalchemy.orm import Session

def get_all_endereco(db: Session):
    return db.query(EnderecoModel).all()

