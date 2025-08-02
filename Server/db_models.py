from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    name = Column(String, primary_key=True)
    password = Column(String)
    login = Column(Boolean, default=True)
    prconfig = Column(JSON, default={})
    register = Column(JSON, default={})
    group = Column(JSON, default={})
    valid = Column(Boolean, default=True)
    pg = Column(String, default="user") # Permission group

class Audit(Base):
    __tablename__ = 'audit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    info = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class VerifyCode(Base):
    __tablename__ = 'verify'
    code = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)