from werkzeug.security import generate_password_hash,check_password_hash


def generate_hashpassword(password):
    return generate_password_hash(password=password)

def chech_hashpassword(password,hashed_password):
    return check_password_hash(hashed_password,password)