from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Text, Float, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy.sql import func

Base = declarative_base()

class PermissionEnum(str, Enum):
    FINANCE = 'finance'
    SUPERADMIN = 'superadmin'
    MARKETING = 'marketing'

class Admin(Base):
    __tablename__ = 'admins'
    admin_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    admin_name = Column(String(50), nullable=False)
    permissions = Column(String(20), nullable=False, server_default=PermissionEnum.SUPERADMIN.value)
    password = Column(String(255), nullable=False)