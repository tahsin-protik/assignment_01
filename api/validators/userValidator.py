from ..utils.db import db
from ..models.user import User
from .errors import Bad_format_of_data
from api import db


class User_validator():
    def __init__(self, args, type="create"):
        username=args.get('username', None)
        first_name=args.get('first_name', None)
        last_name=args.get('last_name', None)
        user_type=args.get('user_type', None)
        street= args.get('street', None)
        city=args.get('city', None)
        state=args.get('state', None)
        zip_code= args.get('zip_code', None)
        parent= args.get('parent', None)

        if type=="create":
            if not username:
                raise Bad_format_of_data(400, "Username Missing")
            else:
                is_exist= User.query.filter_by(username=username).first()
                if is_exist:
                    raise Bad_format_of_data(400, "Username Already Exists")
        else:
            if not username:
                raise Bad_format_of_data(400, "Username Missing")
            else:
                is_exist= User.query.filter_by(username=username).first()
                if not is_exist:
                    raise Bad_format_of_data(400, "User Doesn't Exist")

        if not first_name:
            raise Bad_format_of_data(400, "First Name Missing")
        if not last_name:
            raise Bad_format_of_data(400, "Last Name Missing")
        if not user_type:
            raise Bad_format_of_data(400, "User Type Missing")
        if user_type!= "Parent" and user_type!="Child":
            raise Bad_format_of_data(400, "User Type Not Valid")
        if user_type=="Child":
            if not parent:
                raise Bad_format_of_data(400, "Child User Should Have Parent")
            else:
                is_exist=User.query.filter_by(username=parent).first()
                if not is_exist:
                    raise Bad_format_of_data(400, "Parent Not Valid")
            if street or city or state or zip_code:
                raise Bad_format_of_data(400, "Child User Shouldn't Have Adress")
        
        if user_type=="Parent":
            if not (street and city and state and zip_code) :
                raise Bad_format_of_data(400, "Parent User Should Have Adress")
            if parent:
                raise Bad_format_of_data(400, "Parent User Shouldn't Have Parent")
        



