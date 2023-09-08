from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
import uuid

from sqlalchemy.ext.declarative import declarative_base

from models.usuario import UsuarioModel

print(UsuarioModel.__tablename__)
