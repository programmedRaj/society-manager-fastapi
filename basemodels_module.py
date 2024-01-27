from typing import Optional
from pydantic import BaseModel
from enum import Enum
from fastapi import Query

class FeaturesDBCreate(BaseModel):
    amenity_name: str
    amenity_plan_name: str
    amenity_for: str
    is_paid: bool = False

class UserType(str, Enum):
    SECURITY = 'security'
    SOCIETY_MANAGER = 'society_manager'
    ADMIN = 'admin'
    USER = 'user'

class UserDBCreate(BaseModel):
    phone: str
    user_type: UserType = UserType.USER
    device_token: str
    name: str
    on_duty: bool
    status: bool
    society_id:  Optional[int]  =  Query(None, alias="wing_id")
    wing_id:  Optional[int]  = Query(None, alias="wing_id")

@classmethod
def validate_society_id(cls, society_id):
        return None if society_id == 0 else society_id

@classmethod
def validate_wing_id(cls, wing_id):
    return None if wing_id == 0 else wing_id

class NoticeBoardCreate(BaseModel):
    content: str = 'All important updates will be given here.'
    user_id: int
    wing_id: int

class PermissionEnum(str, Enum):
    FINANCE = 'finance'
    SUPERADMIN = 'superadmin'
    MARKETING = 'marketing'

class AdminCreate(BaseModel):
    user_id: int
    admin_name: str
    permissions: PermissionEnum = PermissionEnum.SUPERADMIN
    password: str

class SocietyCreate(BaseModel):
    society_name: str
    pincode_master_id: int
    address: str
    latitude: float
    longitude: float

class SocietyWingsDetailsCreate(BaseModel):
    society_id: int
    wing_name: str
    amenity_plan_name: str
    notice_id: Optional[int]

class SOSCreate(BaseModel):
    pincode_master_id: int
    SOS_details: dict

class PincodeMasterCreate(BaseModel):
    pincode: int

class SocietyWingsDetailsCreate(BaseModel):
    society_id: int
    wing_name: str
    amenity_plan_name: str
    notice_id: Optional[int]

class SOSCreate(BaseModel):
    pincode_master_id: int
    SOS_details: dict

class PincodeMasterCreate(BaseModel):
    pincode: int

