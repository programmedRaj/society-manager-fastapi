from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Text, Float, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import VARCHAR
import uuid

Base = declarative_base()

association_table = Table('user_features', Base.metadata,
    Column('user_id', VARCHAR(36), ForeignKey('users.user_id'), nullable=False),
    Column('amenity_id', Integer , ForeignKey('features.amenity_id'), nullable=False)
)

class UserFeaturesAssociation(Base):
    __tablename__ = 'user_features_association'
    user_id = Column(VARCHAR(36), ForeignKey('users.user_id'), primary_key=True)
    amenity_id = Column(Integer, ForeignKey('features.amenity_id'), primary_key=True)

class UserDB(Base):
    __tablename__ = 'users'
    user_id =Column(VARCHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    phone = Column(String(15))
    user_type = Column(String(20))
    device_token = Column(String(255))
    name = Column(String(50))
    on_duty = Column(Boolean)
    status = Column(Boolean)
    society_id = Column(Integer, ForeignKey('society.id'), nullable=True, default=None)
    society = relationship("Society", back_populates="users", foreign_keys=[society_id])
    wing_id = Column(Integer, ForeignKey('society_wings_details.wing_id'), nullable=True, default=None)
    wing = relationship("SocietyWingsDetails", back_populates="users", foreign_keys=[wing_id])
    features = relationship("FeaturesDB", secondary=association_table, back_populates="users")
    society_wings_details = relationship("SocietyWingsDetails", back_populates="users")
    notice_board = relationship("NoticeBoard", back_populates="user")

class FeaturesDB(Base):
    __tablename__ = 'features'
    amenity_id = Column(Integer, primary_key=True, nullable=False)
    amenity_name = Column(String(50))
    amenity_plan_name = Column(String(50))
    amenity_for = Column(String(50))
    is_paid = Column(Boolean, default=False)
    users = relationship("UserDB", secondary=association_table, back_populates="features")

class PincodeMaster(Base):
    __tablename__ = 'pincode_master'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pincode = Column(Integer, nullable=False)
    city = Column(String(35))
    district = Column(String(25))
    state = Column(String(15))
    SOS = relationship("SOS", back_populates="pincode_master")

class SOS(Base):
    __tablename__ = 'SOS'
    pincode_master_id = Column(Integer, ForeignKey('pincode_master.id'), primary_key=True)
    SOS_details = Column(JSON, nullable=False)
    pincode_master = relationship("PincodeMaster", back_populates="SOS")

class Society(Base):
    __tablename__ = 'society'
    id = Column(Integer, primary_key=True)
    society_name = Column(String(255), nullable=False)
    pincode_master_id = Column(Integer, ForeignKey('pincode_master.id'), nullable=False)
    address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    pincode_master = relationship("PincodeMaster")
    users = relationship("UserDB", back_populates="society")
    society_wings_details = relationship("SocietyWingsDetails", back_populates="society")

class SocietyWingsDetails(Base):
    __tablename__ = 'society_wings_details'
    society_id = Column(Integer, ForeignKey('society.id'), nullable=False)
    society = relationship("Society", back_populates= "society_wings_details")
    wing_id = Column(Integer, primary_key=True)
    wing_name = Column(String(50), nullable=False)  
    amenity_plan_name = Column(String(50))
    notice_id = Column(VARCHAR(36), ForeignKey('notice_board.notice_id')) 
    notice_board = relationship("NoticeBoard", uselist=False, back_populates="wing")
    users = relationship("UserDB", back_populates="society_wings_details")

class NoticeBoard(Base):
    __tablename__ = 'notice_board'
    notice_id = Column(VARCHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    content = Column(String(2000), nullable=False, default='All important updates will be given here.')
    user_id = Column(VARCHAR(36), ForeignKey('users.user_id'))
    user = relationship("UserDB", back_populates="notice_board")
    wing = relationship("SocietyWingsDetails", back_populates="notice_board")
    last_updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    society_wings_details = relationship("SocietyWingsDetails", back_populates="notice_board")

class PermissionEnum(str, Enum):
    FINANCE = 'finance'
    SUPERADMIN = 'superadmin'
    MARKETING = 'marketing'

class Admin(Base):
    __tablename__ = 'admins'
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    admin_name = Column(String(50), nullable=False)
    permissions = Column(String(20), nullable=False, server_default=PermissionEnum.SUPERADMIN.value)
    password = Column(String(255), nullable=False)