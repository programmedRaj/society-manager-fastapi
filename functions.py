from basemodels_module import *
from database_module import *

def map_user_type_to_amenity_id(user_type):
    user_type_mapping = {
        'user': 1,
        'security': 2,
        'society_manager': 3
    }
    return user_type_mapping.get(user_type, 4)

def user_exists(phone):
    with DBSession() as db:
        return db.query(UserDB).filter(UserDB.phone == phone).first() is not None