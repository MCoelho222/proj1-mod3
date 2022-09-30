from datetime import datetime, timedelta
from src.app.models.user import User
from src.app.models.user import User, user_share_schema, users_roles_share_schema
from src.app.utils import generate_jwt


def create_user(name, email, password, gender_id=None, city_id=None, role_id=None, age=None,\
    phone=None, cep=None, district=None, street=None, number_street=None, complement=None, landmark=None):
    
    try:
        User.seed(
            gender_id=gender_id, 
            city_id=city_id,
            role_id=role_id, 
            name=name, 
            age=age, 
            email=email,
            phone=phone, 
            password=password, 
            cep=cep,
            district=district, 
            street=street, 
            number_street=number_street, 
            complement=complement,
            landmark=landmark
        )

        return {"message": "User created with success."}

    except:
        return {"error": "User not created. Email already exists."}


def make_login(email, password):

    try:
        try:
            user_query = User.query.filter_by(email=email).first_or_404()
        except:
            print('FRFRFRFRFR')
            return {"error": "Invalid fields.", "status_code": 401}
        
        user = user_share_schema.dump(user_query)

        if not user_query.check_password(password):
            return {"error": "Invalid fields.", "status_code": 401}

        payload = {
            "name": user['name'],
            "user_id": user_query.id,
            "exp": datetime.utcnow() + timedelta(days=1),
            "roles": user["role_id"]
        }

        token = generate_jwt(payload)

        return {"token": token}
    except:
        return {"error": "Oops! Something went wrong...", "status_code": 500}


def get_by_id(id):
    user = User.query.filter(User.id==id).first()
    return user_share_schema.dump(user)


def get_user_by_email(email):
    try:
        user_query = User.query.filter_by(email = email).first_or_404()
        user_dict = user_share_schema.dump(user_query)
        return { "id": user_dict['id'], "role": user_dict["role_id"] }

    except:
        return { "error": "Ops! Algo deu errado...", "status_code": 500 }


def get_users_by_name(name, page=None):
    print(name)
    result = User.query.filter(User.name.ilike(f"%{name}%")).paginate(per_page=20, page=page)
    users = users_roles_share_schema.dump(result.items)
        
    return users if result else None

    
def get_all_users(page=None):
    users = users_roles_share_schema.dump(User.query.paginate(per_page=20, page=page).items)
    return users if users else None
