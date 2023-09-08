from fastapi import HTTPException
from models.reserva import ReservaModel
from schemas.reserva import Reserva, ReservaPartial

from sqlalchemy.orm import Session

import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from pydantic import ValidationError

def get_all_reserva(db: Session):
    print("get_all_reserva")
    return db.query(ReservaModel).all()

def create_reserva(db: Session, reserva: Reserva):
    print("create_reserva")
    db_reserva = ReservaModel(**reserva)
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

def update_reserva(db: Session, reserva_id: str, reserva: Reserva):
    print("update_reserva")
    db_reserva = db.query(ReservaModel).filter(ReservaModel.reserva_id == reserva_id).first()
    
    if db_reserva is None:
        raise Exception("Usuário não encontrado")
    
    db.query(ReservaModel).filter(ReservaModel.reserva_id == reserva_id).update(reserva)
    
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

def delete_reserva(db: Session, reserva_id: str):
    print("delete_reserva")
    db_reserva = db.query(ReservaModel).filter(ReservaModel.reserva_id == reserva_id).first()
    
    if db_reserva is None:
        raise Exception("Usuário não encontrado")
    
    db.delete(db_reserva)
    db.commit()
    return db_reserva
